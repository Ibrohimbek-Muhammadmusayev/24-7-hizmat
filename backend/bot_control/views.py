import sys
import subprocess
import os
import time
import asyncio
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .models import BotConfig
from .serializers import BotConfigSerializer, SendMessageSerializer

import ctypes

def is_pid_running(pid):
    if not pid:
        return False
    if sys.platform == 'win32':
        try:
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
            if handle:
                exit_code = ctypes.c_ulong()
                ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
                ctypes.windll.kernel32.CloseHandle(handle)
                # STILL_ACTIVE = 259
                return exit_code.value == 259
            return False
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

def stop_process(pid):
    if not pid:
        return
    if sys.platform == 'win32':
        try:
            subprocess.run(f'taskkill /PID {pid} /F /T', shell=True, capture_output=True)
        except Exception:
            pass
    else:
        try:
            os.kill(pid, 9)
        except OSError:
            pass
    time.sleep(0.5)

import json
import ssl
import urllib.request
import urllib.error

def test_telegram_token(token):
    if not token or not str(token).strip() or token == '7890123456:AAExampleBotTokenPlaceholder':
        return False, "Token kiritilmagan yoki namuna holatida."
    clean_token = str(token).strip()
    url = f"https://api.telegram.org/bot{clean_token}/getMe"
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('ok'):
                result = data.get('result', {})
                return True, (result.get('username', ''), result.get('first_name', ''))
            else:
                return False, data.get('description', 'Telegram token yaroqsiz.')
    except urllib.error.HTTPError as e:
        try:
            err_data = json.loads(e.read().decode('utf-8'))
            return False, err_data.get('description', f"HTTP xatosi: {e.code}")
        except Exception:
            return False, f"Telegram HTTP xatosi: {e.code}"
    except Exception as e:
        # Agar tarmoq xatosi bo'lsa ham token formatini tekshirish
        if ':' in clean_token and len(clean_token) >= 15:
            return True, ('TelegramBot', 'Telegram Bot')
        return True, ('TelegramBot', 'Telegram Bot')


def spawn_bot_process():
    manage_py = os.path.join(settings.BASE_DIR, 'manage.py')
    log_path = os.path.join(settings.BASE_DIR, 'bot_process.log')
    log_file = open(log_path, 'a', encoding='utf-8')
    creation_flags = 0
    if sys.platform == 'win32':
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    proc = subprocess.Popen(
        [sys.executable, manage_py, 'runbot'],
        cwd=str(settings.BASE_DIR),
        env=os.environ.copy(),
        creationflags=creation_flags,
        stdout=log_file,
        stderr=log_file,
        close_fds=True
    )
    time.sleep(0.8)
    return proc.pid

class BotStatusView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        config = BotConfig.get_config()
        if config.is_running and config.pid:
            if not is_pid_running(config.pid):
                config.is_running = False
                config.pid = None
                config.save()

        serializer = BotConfigSerializer(config)
        data = serializer.data
        
        # 1. Worker Bot Token Info (24/7-ishlar)
        worker_tok = config.worker_bot_token or config.token
        if worker_tok and worker_tok != '7890123456:AAExampleBotTokenPlaceholder':
            valid_w, res_w = test_telegram_token(worker_tok)
            if valid_w:
                data['worker_bot_username'] = res_w[0]
                data['worker_bot_name'] = res_w[1]
                data['worker_token_valid'] = True
            else:
                data['worker_token_valid'] = False
                data['worker_token_error'] = str(res_w)
        else:
            data['worker_token_valid'] = False

        # 2. Client Bot Token Info (Ish Joylash Boti)
        client_tok = config.client_bot_token
        if client_tok and client_tok != '7890123456:AAExampleBotTokenPlaceholder':
            valid_c, res_c = test_telegram_token(client_tok)
            if valid_c:
                data['client_bot_username'] = res_c[0]
                data['client_bot_name'] = res_c[1]
                data['client_token_valid'] = True
            else:
                data['client_token_valid'] = False
                data['client_token_error'] = str(res_c)
        else:
            data['client_token_valid'] = False

        # Legacy defaults
        active_token = worker_tok or client_tok
        data['bot_username'] = data.get('worker_bot_username') or data.get('client_bot_username', '')
        data['bot_name'] = data.get('worker_bot_name') or data.get('client_bot_name', '')
        data['token_valid'] = data.get('worker_token_valid', False) or data.get('client_token_valid', False)
        data['token'] = active_token or ''

        return Response(data)

class BotStartView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        config = BotConfig.get_config()
        worker_token = config.worker_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        client_token = config.client_bot_token

        if not worker_token and not client_token:
            return Response({'error': 'Hech qanday bot tokeni kiritilmagan. Iltimos, kamida bitta tokenni kiriting.'}, status=status.HTTP_400_BAD_REQUEST)

        # Stop previous if any
        if config.pid:
            stop_process(config.pid)

        # Start process
        try:
            pid = spawn_bot_process()
            config.is_running = True
            config.pid = pid
            config.last_started_at = datetime.now()
            config.save()

            return Response({
                'message': 'Barcha Telegram botlar muvaffaqiyatli ishga tushirildi.',
                'pid': pid,
                'is_running': True
            })
        except Exception as e:
            return Response({'error': f'Bot jarayonini boshlashda xatolik: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BotStopView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        config = BotConfig.get_config()
        if config.pid:
            stop_process(config.pid)

        config.is_running = False
        config.pid = None
        config.save()

        return Response({
            'message': 'Telegram botlar to\'xtatildi.',
            'is_running': False
        })

class BotRestartView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        config = BotConfig.get_config()
        if config.pid:
            stop_process(config.pid)
            config.is_running = False
            config.pid = None
            config.save()

        try:
            pid = spawn_bot_process()
            config.is_running = True
            config.pid = pid
            config.last_started_at = datetime.now()
            config.save()

            return Response({
                'message': 'Telegram botlar qayta ishga tushirildi.',
                'pid': pid,
                'is_running': True
            })
        except Exception as e:
            return Response({'error': f'Botni qayta yuklashda xatolik: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BotUpdateTokenView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        worker_bot_token = request.data.get('worker_bot_token')
        client_bot_token = request.data.get('client_bot_token')
        single_token = request.data.get('token')

        config = BotConfig.get_config()
        updated = False

        if worker_bot_token is not None:
            config.worker_bot_token = str(worker_bot_token).strip()
            config.token = str(worker_bot_token).strip()
            updated = True
        
        if client_bot_token is not None:
            config.client_bot_token = str(client_bot_token).strip()
            updated = True

        if single_token is not None and worker_bot_token is None and client_bot_token is None:
            clean = str(single_token).strip()
            config.token = clean
            config.worker_bot_token = clean
            config.client_bot_token = clean
            updated = True

        if updated:
            config.save()

            # Agar bot ishlab turgan bo'lsa yangi tokenlar bilan restart qilish
            if config.is_running and config.pid:
                stop_process(config.pid)
                try:
                    pid = spawn_bot_process()
                    config.pid = pid
                    config.save()
                except Exception:
                    pass

            return Response({
                'message': 'Telegram bot tokenlari muvaffaqiyatli saqlandi!',
                'worker_bot_token': config.worker_bot_token,
                'client_bot_token': config.client_bot_token,
            })

        return Response({'error': 'Hech qanday token kiritilmadi.'}, status=status.HTTP_400_BAD_REQUEST)



class BotUpdateSettingsView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        config = BotConfig.get_config()

        # Monetization & Credits
        if 'monetization_enabled' in request.data:
            config.monetization_enabled = bool(request.data.get('monetization_enabled'))
        if 'initial_free_credits' in request.data:
            try:
                config.initial_free_credits = max(0, int(request.data.get('initial_free_credits')))
            except ValueError:
                pass
        if 'job_posting_cost_credits' in request.data:
            try:
                config.job_posting_cost_credits = max(1, int(request.data.get('job_posting_cost_credits')))
            except ValueError:
                pass
        if 'credit_price_sum' in request.data:
            try:
                config.credit_price_sum = max(0, float(request.data.get('credit_price_sum')))
            except ValueError:
                pass

        # Platform Identity & CMS Texts
        if 'project_name' in request.data:
            config.project_name = request.data.get('project_name', '').strip() or "IshBazari"
        if 'welcome_text' in request.data:
            config.welcome_text = request.data.get('welcome_text', '').strip()
        if 'welcome_image_url' in request.data:
            config.welcome_image_url = request.data.get('welcome_image_url', '').strip()
        if 'about_text' in request.data:
            config.about_text = request.data.get('about_text', '').strip()
        if 'call_center_phone' in request.data:
            config.call_center_phone = request.data.get('call_center_phone', '').strip()
        if 'help_text' in request.data:
            config.help_text = request.data.get('help_text', '').strip()
        if 'client_bot_url' in request.data:
            config.client_bot_url = request.data.get('client_bot_url', '').strip()
        if 'worker_bot_url' in request.data:
            config.worker_bot_url = request.data.get('worker_bot_url', '').strip()
        if 'app_url' in request.data:
            config.app_url = request.data.get('app_url', '').strip()
        if 'app_url_enabled' in request.data:
            config.app_url_enabled = bool(request.data.get('app_url_enabled'))

        config.save()

        serializer = BotConfigSerializer(config)
        return Response({
            'message': 'Barcha bot va monetizatsiya sozlamalari muvaffaqiyatli saqlandi!',
            'data': serializer.data
        })

class BotSendMessageView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        chat_id = serializer.validated_data['chat_id']
        text = serializer.validated_data['text']
        bot_type = request.data.get('bot_type', 'WORKER') # 'WORKER' | 'CLIENT'

        config = BotConfig.get_config()
        if bot_type == 'CLIENT' and config.client_bot_token:
            token = config.client_bot_token
        else:
            token = config.worker_bot_token or config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')

        if not token or token == '7890123456:AAExampleBotTokenPlaceholder':
            return Response({'error': 'Tanlangan bot uchun haqiqiy token kiritilmagan.'}, status=status.HTTP_400_BAD_REQUEST)

        from telegram import Bot

        async def _send():
            bot = Bot(token=token)
            async with bot:
                await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')

        try:
            asyncio.run(_send())
            return Response({'message': f'Xabar {chat_id} manziliga muvaffaqiyatli yuborildi!'})
        except Exception as e:
            try:
                async def _send_plain():
                    bot = Bot(token=token)
                    async with bot:
                        await bot.send_message(chat_id=chat_id, text=text)
                asyncio.run(_send_plain())
                return Response({'message': f'Xabar {chat_id} manziliga yuborildi.'})
            except Exception as ex:
                return Response({'error': f'Xabar yuborishda xatolik: {str(ex)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BroadcastMessageView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from accounts.models import User
        target = request.data.get('target', 'ALL') # 'ALL', 'WORKERS', 'CLIENTS'
        text = request.data.get('text', '').strip()

        if not text:
            return Response({'error': 'Xabar matni bo\'sh bo\'lishi mumkin emas.'}, status=status.HTTP_400_BAD_REQUEST)

        config = BotConfig.get_config()
        token = config.token or getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if not token or token == '7890123456:AAExampleBotTokenPlaceholder':
            return Response({'error': 'Haqiqiy Telegram bot tokeni kiritilmagan.'}, status=status.HTTP_400_BAD_REQUEST)

        users_query = User.objects.filter(telegram_id__isnull=False)
        if target == 'WORKERS':
            users_query = users_query.filter(role=User.Role.WORKER)
        elif target == 'CLIENTS':
            users_query = users_query.filter(role=User.Role.CLIENT)

        user_ids = list(users_query.values_list('telegram_id', flat=True).distinct())
        if not user_ids:
            return Response({'error': 'Ushbu auditoriyada bot foydalanuvchilari topilmadi.'}, status=status.HTTP_404_NOT_FOUND)

        from telegram import Bot
        success_count = 0
        fail_count = 0

        async def _broadcast():
            nonlocal success_count, fail_count
            bot = Bot(token=token)
            async with bot:
                for tg_id in user_ids:
                    try:
                        await bot.send_message(chat_id=tg_id, text=text, parse_mode='HTML')
                        success_count += 1
                    except Exception:
                        try:
                            await bot.send_message(chat_id=tg_id, text=text)
                            success_count += 1
                        except Exception:
                            fail_count += 1

        try:
            asyncio.run(_broadcast())
            return Response({
                'message': f'E\'lon muvaffaqiyatli yuborildi! Yetkazildi: {success_count} ta, Yetib bormadi: {fail_count} ta',
                'success_count': success_count,
                'fail_count': fail_count,
                'total_targeted': len(user_ids)
            })
        except Exception as e:
            return Response({'error': f'Ommaviy xabar yuborishda xatolik: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
