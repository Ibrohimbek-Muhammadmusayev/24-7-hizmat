TEXTS = {
    'uz': {
        'choose_lang': "Assalomu alaykum! Iltimos, muloqot tilini tanlang:",
        'lang_selected': "🇺🇿 O'zbek tili (Lotin) tanlandi.",
        'welcome_back': "Assalomu alaykum, <b>{name}</b>! 👋\n\n<b>{project_name}</b> platformasiga xush kelibsiz!\nQuyidagi menyu orqali kerakli bo'limni tanlang:",
        
        # 0.1-Qadam: Rol
        'choose_role': "Quyidagi variantlardan birini tanlang:",
        'role_worker': "🛠 Ish qidiryapman / Usta sifatida kirish",
        'role_client': "📢 Ishchi qidiryapman / Ish joylash",
        'client_redirect_msg': "🚀 <b>Ish beruvchilar boti</b>\n\nIsh yoki vakansiya e'lon qilish uchun rasmiy ish beruvchilar botimizga o'ting:",
        'btn_goto_client_bot': "🚀 Ish beruvchi botiga o'tish",

        # 1-Qadam: Shaxsiy ma'lumotlar
        'step1_gender_title': "1-QADAM: SHAXSIY MA'LUMOTLAR\n\n1.1 Jinsingizni tanlang:",
        'gender_male': "👨 Erkak",
        'gender_female': "👩 Ayol",
        'step1_name_title': "1.2 Ism va Familiyangizni kiriting:\n<i>(Masalan: Ali Valiyev)</i>",
        'step1_age_title': "1.3 Yoshingizni kiriting:\n<i>(Faqat son kiriting, masalan: 25)</i>",
        'step1_age_invalid': "⚠️ Iltimos, yoshingizni to'g'ri musbat butun sonda kiriting (masalan: 25):",
        'step1_phone_title': "1.4 Telefon raqamingizni yuboring yoki quyidagi formatda kiriting (+998901234567):",
        'btn_send_phone': "📱 Telefon raqamni ulashish",
        'step1_phone_invalid': "⚠️ Telefon raqami noto'g'ri. Iltimos, tugmani bosing yoki +998XXXXXXXXX formatida kiriting:",

        # 2-Qadam: Manzil va Joylashuv
        'step2_geo_title': "2-QADAM: MANZIL VA JOYLASHUV\n\n2.1 GPS Lokatsiyangizni yuboring:\n<i>(Tizim avtomatik viloyat va tumanni aniqlaydi)</i>",
        'btn_send_gps': "📍 Lokatsiyani yuborish",
        'btn_manual_region': "🏛 Viloyatni qo'lda tanlash",
        'step2_address_title': "2.2 Aniq manzilingizni kiriting:\n<i>(Mahalla / Ko'cha va Uy/xonadon raqami)</i>",
        'choose_region_worker': "📍 Qaysi hududda ish qidirmoqchisiz?\nViloyatni tanlang:",

        # 3-Qadam: Kasb va Xizmat yo'nalishlari
        'choose_category': "3-QADAM: KASB VA XIZMAT YO'NALISHLARI\n\n3.1 Asosiy sohani tanlang:\n(Sahifa {current}/{total})",
        'choose_position': "3.2 Mutaxassisliklarni tanlang (10 tagacha tanlash mumkin):\n(Sahifa {current}/{total})\n\nTanlanganlar: {selected_count}/10 ta",
        'max_pos_alert': "⚠️ Siz maksimal 10 ta mutaxassislik tanlashingiz mumkin!",
        'btn_continue': "➡️ Keyingi qadamga o'tish ({count} ta)",
        'btn_choose_other_cats': "➕ Boshqa sohalardan ham tanlash",
        'btn_back_to_cats': "📂 Sohalar ro'yxatiga qaytish",
        'btn_back': "⬅️ Orqaga",

        # 4-Qadam: Ish rejimi va Shartlari
        'step4_emp_type_title': "4-QADAM: ISH REJIMI VA SHARTLARI\n\n4.1 Qaysi bandlik turida ishlamoqchisiz?",
        'emp_type_daily': "⚡️ Bir martalik / Kunbay",
        'emp_type_permanent': "💼 Doimiy ish",
        'emp_type_both': "🔄 Ikkalasi ham",
        'step4_schedule_title': "4.2 Ish vaqti rejimini tanlang:",
        'schedule_day': "☀️ 09:00 - 18:00 (Kunduzgi)",
        'schedule_24_7': "🚨 24/7 (Istalgan vaqtda / Shoshilinch)",
        'schedule_flexible': "⏱ Erkin grafik",

        # 5-Qadam: Profilni tasdiqlash
        'step5_review_title': "📋 <b>5-QADAM: PROFILNI TASDIQLASH</b>\n\nIltimos, kiritilgan ma'lumotlarni tekshiring:\n\n👤 <b>F.I:</b> {name} ({gender}, {age} yosh)\n📞 <b>Tel:</b> {phone}\n📍 <b>Hudud:</b> {region}, {district}\n🏠 <b>Aniq manzil:</b> {street_address}\n🛠 <b>Tanlangan sohalar va mutaxassisliklar ({pos_count} ta):</b>\n{positions}\n💼 <b>Bandlik turi:</b> {emp_type}\n⏱ <b>Ish rejimi:</b> {work_schedule}\n\nMa'lumotlar to'g'rimi?",
        'btn_confirm_profile': "✅ Tasdiqlash",
        'btn_restart_profile': "🔄 Qaytadan kiritish",
        'reg_success': "✅ Tabriklaymiz! Sizning anketangiz muvaffaqiyatli saqlandi va profilingiz faollashtirildi.",

        # ASOSIY MENYU TUZILISHI
        'main_menu': "🏠 <b>{project_name} — Asosiy menyu</b>\n\n👤 <b>Usta:</b> {name}\n📍 <b>Hudud:</b> {location}\n🛠 <b>Sohalar:</b> {positions}\n{status_badge}\n\nQuyidagi bo'limlardan birini tanlang:",
        'status_active_badge': "🟢 <b>Holat:</b> Faol (Buyurtmalar qabul qilinmoqda)",
        'status_busy_badge': "🔴 <b>Holat:</b> Band (Yangi ishlar to'xtatilgan)",
        
        # 1. ISHLARNI KO'RISH / QIDIRISH
        'btn_menu_jobs': "🔎 ISHLARNI KO'RISH / QIDIRISH",
        'jobs_menu_title': "🔎 <b>ISHLARNI QIDIRISH VA KO'RISH</b>\n\nQanday usulda ish qidirmoqchisiz?",
        'btn_jobs_matched': "📋 Barcha ishlar",
        'btn_jobs_by_cat': "🔍 Kategoriya bo'yicha izlash",
        'btn_jobs_by_geo': "🗺 Hudud bo'yicha izlash",
        'jobs_empty': "🔍 Hozirda sizning mezonlaringiz bo'yicha yangi buyurtmalar yo'q.\n\n🔔 Yangi e'lon qo'shilishi bilan sizga bildirishnoma yuboriladi!",
        'job_card_text': "📄 <b>E'lon #{id} ({current}/{total}):</b>\n\n📋 <b>{category} / {service_type}</b>\n📍 <b>Manzil:</b> {address}\n⏱ <b>Vaqt:</b> {work_time} ({work_format})\n💰 <b>Haq:</b> {price}\n📝 <b>Tavsif:</b> {desc}\n\n📞 <b>Ish beruvchi:</b> {customer_name}",
        'btn_take_job': "💼 Ishni olish",
        'btn_check_job_status': "🔍 Faolligini tekshirish",
        'btn_refresh_jobs': "🔄 Sahifani yangilash",
        'btn_cancel': "❌ Bekor qilish",
        'btn_contact_employer': "📞 Ish beruvchi bilan bog'lanish",
        'btn_next_job': "➡️ Keyingi ({current}/{total})",
        'btn_prev_job': "⬅️ Oldingi ({current}/{total})",
        'btn_geo_district': "🏛 Faqat o'z tumanim",
        'btn_geo_region': "📍 Butun viloyat",
        'btn_geo_radius_5': "🎯 Radius 5 km",
        'btn_geo_radius_10': "🎯 Radius 10 km",
        'btn_geo_radius_25': "🎯 Radius 25 km",
        'job_status_active_alert': "✅ Ushbu e'lon ayni paytda FAOL va qabul qilish uchun ochiq!",
        'job_status_taken_alert': "⚠️ Kechirasiz, ushbu ish boshqa mutaxassis tomonidan olingan yoki biriktirilgan!",
        'job_status_closed_alert': "❌ Ushbu ish e'loni ish beruvchi tomonidan olib tashlangan yoki yopilgan!",
        'job_already_applied_alert': "ℹ️ Siz allaqachon ushbu ish bo'yicha so'rov yuborgansiz. Ish beruvchi javobini kuting!",
        'prompt_apply_message': "✍️ <b>Ish beruvchiga taklif / xabar yuborish:</b>\n\nE'lon: <b>#{job_id} — {title}</b>\n\nIsh beruvchiga o'zingiz haqingizda qisqacha ma'lumot, narx yoki qachon yetib bora olishingiz haqida xabar yozib yuboring:\n<i>(Masalan: Assalomu alaykum, men 5 yillik tajribali ustaman, 30 daqiqada yetib boraman)</i>",
        'apply_confirm_title': "📋 <b>SO'ROVNI TASDIQLASH:</b>\n\n📢 <b>E'lon:</b> #{job_id} — {title}\n✉️ <b>Sizning xabaringiz:</b>\n<i>\"{msg}\"</i>\n\nIsh beruvchiga yuborilsinmi?",
        'btn_send_proposal': "🚀 Yuborish",
        'btn_edit_proposal': "✏️ O'zgartirish",
        'btn_cancel_proposal': "❌ Bekor qilish",
        'apply_success_msg': "🎉 <b>So'rovingiz ish beruvchiga muvaffaqiyatli yuborildi!</b>\n\nIsh beruvchi xabaringizni ko'rib chiqib siz bilan bog'lanadi yoki javob qaytaradi. Iltimos, javob kelishini kuting.",

        # 2. MENING PROFILIM (KABINET)
        'btn_menu_profile': "👤 MENING PROFILIM (KABINET)",
        'cabinet_title': "👤 <b>USTA PROFILI KABINETI:</b>\n\n👤 <b>F.I.Sh:</b> {name} ({age} yosh, {gender})\n📞 <b>Tel:</b> {phone}\n📍 <b>Joylashuv:</b> {region}, {district}\n🏠 <b>Aniq manzil:</b> {street_address}\n🛠 <b>Sohalar ({pos_count}/10):</b>\n{positions}\n⏱ <b>Rejim:</b> {work_schedule} | {emp_type}\n{status_badge}\n⭐️ <b>Reyting:</b> {rating} / 5.0 ({reviews_count} ta sharh)\n✅ <b>Bajarilgan ishlar:</b> {completed_count} ta",
        'btn_edit_profile': "✏️ Ma'lumotlarni tahrirlash",
        'btn_portfolio': "🖼 Ish namunalarim (Portfolio)",
        'edit_menu_title': "✏️ <b>Qaysi ma'lumotingizni o'zgartirmoqchisiz?</b>",
        'btn_edit_name_age': "👤 F.I.Sh va Yoshni o'zgartirish",
        'btn_edit_phone': "📞 Telefon raqamni yangilash",
        'btn_edit_location': "📍 Manzil / Lokatsiyani qayta yuborish",
        'btn_edit_positions': "🛠 Mutaxassisliklarni tahrirlash",
        
        # Portfolio
        'portfolio_title': "🖼 <b>ISH NAMUNALARINGIZ (PORTFOLIO):</b>\n\nYuklangan ishlar soni: <b>{count}/5 ta</b>\n\nUshbu namunalar buyurtmachi va mijozlarga sizning mahoratingiz va tajribangizni ko‘rsatish uchun xizmat qiladi.",
        'btn_add_portfolio_item': "➕ Yangi namuna qo‘shish",
        'btn_view_portfolio_items': "👀 Namunalarimni ko‘rish ({count} ta)",
        'prompt_upload_portfolio_photo': "📸 <b>Yangi namuna qo‘shish (1/2):</b>\n\nIltimos, bajargan ishingiz rasmini yuboring:",
        'prompt_upload_portfolio_caption': "📝 <b>Yangi namuna qo‘shish (2/2):</b>\n\nUshbu ish namunasi haqida qisqacha izoh/tavsif yozib yuboring:\n<i>(Masalan: Qo‘shtepa tumanida 2 qavatli uy devori, pishiq g‘ishtdan terilgan)</i>",
        'prompt_edit_caption': "✏️ <b>Izohni tahrirlash:</b>\n\nUshbu namuna uchun yangi izoh matnini yozib yuboring:",
        'prompt_replace_photo': "🔄 <b>Rasmni almashtirish:</b>\n\nUshbu namuna uchun yangi rasmni yuboring (eski izoh saqlanib qoladi):",
        'portfolio_item_card': "📸 <b>ISH NAMUNASI</b>\n📌 <b>{current} / {total} - namuna</b>\n\n📝 <b>Izoh:</b> {caption}",
        'portfolio_item_no_caption': "Kiritilmagan",
        'btn_prev_item': "⬅️ Oldingi",
        'btn_next_item': "Keyingi ➡️",
        'btn_edit_caption': "✏️ Izohni tahrirlash",
        'btn_replace_photo': "🔄 Rasmni almashtirish",
        'btn_delete_item': "🗑 Ushbu namunani o‘chirish",
        'btn_back_to_portfolio': "🖼 Portfolioga qaytish",
        'photo_uploaded_success': "✅ Yangi ish namunasi portfoliosingizga muvaffaqiyatli qo‘shildi! ({count}/5 ta)",
        'photo_replaced_success': "✅ Namuna rasmi muvaffaqiyatli almashtirildi!",
        'caption_updated_success': "✅ Namuna izohi muvaffaqiyatli yangilandi!",
        'photo_deleted_success': "🗑 Namuna muvaffaqiyatli o‘chirildi.",
        'portfolio_full': "⚠️ Siz maksimal 5 ta portfolio namunasi yuklashingiz mumkin.",
        'portfolio_empty': "Sizda hali ish namunalari yuklanmagan.",

        # 3. BANDLIK HOLATI (TOGGLE)
        'btn_menu_toggle_status': "🟢/🔴 BANDLIK HOLATI",
        'status_active_msg': "🟢 <b>Siz hozir FAOL holatdasiz!</b>\n\nYangi buyurtmalar va mijozlar siz bilan bemalol bog'lana oladi hamda bildirishnomalar kelib turadi.",
        'btn_set_busy': "🔴 Band rejimiga o'tish",
        'status_busy_msg': "🔴 <b>Siz BAND holatdasiz!</b>\n\nTizim sizga vaqtincha yangi buyurtmalar yubormaydi va profilingiz band deb ko'rsatiladi.",
        'btn_set_active': "🟢 Faol rejimga o'tish",

        # 4. REYTING VA SHARHLAR
        'btn_menu_reviews': "⭐️ MENING BAHOLARIM VA SHARHLAR",
        'reviews_title': "⭐️ <b>REYTING VA SHARHLAR HISOBOTI:</b>\n\n⭐️ <b>O‘rtacha ball:</b> {rating} / 5.0 ({reviews_count} ta baho)\n✅ <b>Muvaffaqiyatli bajarilgan ishlar:</b> {completed_count} ta\n\n💬 <b>Mijozlar qoldirgan so‘nggi sharhlar:</b>",
        'reviews_empty': "Hozircha sharhlar mavjud emas.",
        'review_item': "💬 <b>{client_name}</b> ({rating} ⭐️):\n<i>\"{comment}\"</i>\n🕒 {date}\n",

        # 4.5. JAVOBLAR (YUBORILGAN SO'ROVLAR VA TAKLIF QILINGAN ISHLAR)
        'btn_menu_applications': "Javoblar / Takliflar",
        'my_applications_title': "👥 <b>SO'ROVLAR VA ISH TAKLIFLARI ({count} ta):</b>\n\nQuyidagi e'lonlarga taklif yuborgansiz yoki sizga ish taklif qilingan:\n<i>(Sahifa {current}/{total})</i>",
        'my_applications_empty': "📬 <b>Hozircha sizda hech qanday so'rov yoki yangi ish takliflari yo'q.</b>\n\n'Ishlarni ko'rish' bo'limiga o'tib o'zingizga mos ishlarga taklif yuborishingiz mumkin!",
        'my_app_detail_card': (
            "📋 <b>ISH MA'LUMOTI VA SO'ROV HOLATI</b>\n"
            "📢 <b>E'lon:</b> #{job_id} — {job_title}\n"
            "📊 <b>Holat:</b> {status_label}\n"
            "🕒 <b>Vaqti:</b> {applied_at}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📍 <b>Ish manzili:</b> {address}\n"
            "💰 <b>Ish haqi:</b> {price}\n"
            "⏱ <b>Vaqt / Format:</b> {work_time} ({work_format})\n"
            "📝 <b>Ish tavsifi:</b> {desc}\n\n"
            "✉️ <b>Taklif / xabar:</b>\n<i>\"{proposal_msg}\"</i>"
            "{contact_section}"
        ),
        'btn_view_application': "👥 Javobni ko'rish",
        'btn_delete_application': "🗑 O'chirish",
        'btn_accept_invited_job': "💼 Ishni qabul qilish / Taklif yuborish",
        'app_deleted_success': "🗑 Ushbu ish so'rovlaringiz ro'yxatidan olib tashlandi.",
        'btn_menu_update_gps': "📍 GPSni yangilash",
        'prompt_send_gps_update': "📍 <b>GPS JOYLAHUVNI YANGILASH:</b>\n\nIltimos, yangi joylashuvingizni (GPS lokatsiya) yuboring.\nTizim sizga yaqin masofadagi (5 km gacha bo'lgan) va hududingizdagi barcha yangi e'lonlarni yetkazadi:",
        'gps_updated_success': "✅ <b>GPS joylashuvingiz muvaffaqiyatli yangilandi!</b>\n\n📍 <b>Hudud:</b> {region}, {district}\n🌐 <b>Koordinata:</b> {gps}\n\nEndi sizga yaqin atrofda joylangan barcha yangi ish buyurtmalari avtomatik tarzda yetkaziladi.",

        # 5. SOZLAMALAR
        'btn_menu_settings': "⚙️ SOZLAMALAR",
        'settings_title': "⚙️ <b>SOZLAMALAR BO'LIMI:</b>\n\nKerakli parametrni tanlang:",
        'btn_settings_lang': "🌐 Tilni o‘zgartirish",
        'btn_settings_notif': "🔔 Bildirishnomalar",
        'notif_title': "🔔 <b>Bildirishnoma rejimini tanlang:</b>\nHozirgi holat: <b>{current}</b>",
        'notif_opt_all': "🔔 Barcha xabarlar yoqiq",
        'notif_opt_night': "🌙 Tungi rejim (22:00 dan keyin ovozsiz)",
        'notif_opt_off': "🔕 Bildirishnomalarni butunlay o‘chirish",
        'notif_saved': "✅ Bildirishnoma sozlamasi saqlandi!",

        # 6. QO'LLAB-QUVVATLASH
        'btn_menu_support': "📞 QO‘LLAB-QUVVATLASH",
        'support_title': "📞 <b>QO‘LLAB-QUVVATLASH VA YORDAM:</b>\n\nPlatformadan foydalanish bo‘yicha savollaringiz yoki takliflaringiz bormi?\n\n📞 <b>Call-markaz:</b> {phone}\n⏰ <b>Ish vaqti:</b> 09:00 dan 18:00 gacha\n\nQuyidagi tugmalar orqali administrator bilan bog'lanishingiz mumkin:",
        'btn_write_admin': "👨‍💻 Administratorga yozish",
        'btn_guide': "📖 Foydalanish qo‘llanmasi",
        'guide_text': (
            "📖 <b>{project_name} BOTIDAN FOYDALANISH QO‘LLANMASI</b>\n\n"
            "Ushbu bot orqali siz o‘z sohangiz bo‘yicha yangi ish buyurtmalarini topishingiz, mijozlar bilan to‘g‘ridan-to‘g‘ri bog‘lanishingiz va shaxsiy profilingizni boshqarishingiz mumkin.\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔘 <b>ASOSIY BO‘LIMLAR VA ULARNING VAZIFASI:</b>\n\n"
            "1️⃣ <b>🔎 ISHLARNI KO‘RISH / QIDIRISH:</b>\n"
            "• <b>📋 Barcha ishlar:</b> Barcha faol buyurtmalar va ish e'lonlari ro'yxati.\n"
            "• <b>🔍 Kategoriya bo‘yicha:</b> Istalgan sohani tanlab, o‘sha sohadagi mavjud barcha e'lonlarni ko‘rish.\n"
            "• <b>🗺 Geografik joylashuv bo‘yicha:</b> O‘z tumaningiz, butun viloyat yoki GPS lokatsiyangizdan 5km, 10km, 25km radiusdagi ishlarni saralash.\n\n"
            "2️⃣ <b>👤 MENING PROFILIM (KABINET):</b>\n"
            "• Shaxsiy ma'lumotlaringiz (ism, yosh, telefon, manzil, sohalar, ish jadvali)ni ko‘rish.\n"
            "• <b>✏️ Tahrirlash:</b> Ma'lumotlar o‘zgarganda ism, telefon, GPS manzil yoki mutaxassisliklarni yangilash.\n"
            "• <b>🖼 Portfoliolarim:</b> Bajarilgan ishlaringizdan 5 tagacha sifatli rasmlar yuklab, mijozlarga namoyish etish.\n\n"
            "3️⃣ <b>🟢/🔴 BANDLIK HOLATI:</b>\n"
            "• <b>🟢 Faol rejim:</b> Siz buyurtmalarni qabul qilishga tayyorsiz. Mijozlar sizni qidiruvda ko‘rishadi.\n"
            "• <b>🔴 Band rejim:</b> Agar hozir ish bilan band bo‘lsangiz yoki dam olayotgan bo‘lsangiz, ushbu rejimni yoqing (sizga yangi xabarlar kelmay turadi).\n\n"
            "4️⃣ <b>⭐️ REYTING VA SHARHLAR:</b>\n"
            "• Buyurtmalarni bajarganingizdan so‘ng mijozlar tomonidan qoldirilgan baholar (1-5 yulduz) va fikr-mulohazalarni kuzatib borish.\n\n"
            "5️⃣ <b>⚙️ SOZLAMALAR:</b>\n"
            "• Muloqot tilini (Lotin, Kirill, Rus, Ingliz) o‘zgartirish.\n"
            "• Bildirishnomalarni boshqarish (barchasi yoqiq, tungi rejim yoki o‘chiq).\n\n"
            "6️⃣ <b>📞 QO‘LLAB-QUVVATLASH:</b>\n"
            "• Operator yoki administrator bilan bog‘lanish, taklif va shikoyatlarni yuborish.\n\n"
            "💡 <i>Eslatma: Doimiy ravishda ko‘proq va daromadli ishlar topish uchun profilingizni to‘liq to‘ldiring va portfoliongizga rasmlar joylang!</i>"
        ),
        'btn_leave_feedback': "💬 Taklif / Shikoyat qoldirish",
        'prompt_feedback': "✍️ Iltimos, o'z taklif yoki shikoyatingizni yozib yuboring. Xabaringiz to'g'ridan-to'g'ri administratorga yetkaziladi:",
        'feedback_received': "✅ Rahmat! Sizning xabaringiz administratorga yuborildi. Tez orada ko'rib chiqiladi.",

        # Umumiy tugmalar va Xatolik / Fallback
        'btn_back_main': "⬅️ Asosiy menyuga qaytish",
        'btn_goto_main_menu': "🏠 Bosh sahifaga qaytish",
        'btn_restart_bot': "🔄 Botni qayta ishga tushirish (/start)",
        'btn_back': "⬅️ Orqaga",
        'bot_error_msg': "⚠️ <b>Kechirasiz, tizimda nosozlik yuz berdi!</b>\n\nBotni qaytadan to'liq ishga tushirish uchun quyidagi buyruqni bosing:\n\n👉 <b>/start</b>",
        'bot_outdated_button_msg': "🔄 <b>Tizim yangilandi / sessiya eskirgan</b>\n\nDavom etish va botni yangilash uchun quyidagi buyruqni bosing:\n\n👉 <b>/start</b>",
        'bot_restarted_notification': "🚀 <b>{project_name} boti yangilandi!</b>\n\n⚙️ Tizimda yangilanishlar amalga oshirildi va barcha xizmatlar barqaror ishlamoqda.\n\nBotdan foydalanishni davom ettirish uchun bosing:\n👉 <b>/start</b>",
    },
    'oz': {
        'choose_lang': "Ассалому алайкум! Илтимос, мулоқот тилини танланг:",
        'lang_selected': "🇺🇿 Ўзбек тили (Кирилл) танланди.",
        'welcome_back': "Ассалому алайкум, <b>{name}</b>! 👋\n\n<b>24/7-ишлар</b> платформасига хуш келибсиз!\nҚуйидаги меню орқали керакли бўлимни танланг:",
        
        # 0.1-Qadam: Rol
        'choose_role': "Қуйидаги вариантлардан бирини танланг:",
        'role_worker': "🛠 Иш қидиряпман / Уста сифатида кириш",
        'role_client': "📢 Ишчи қидиряпман / Иш жойлаш",
        'client_redirect_msg': "🚀 <b>Иш берувчилар боти</b>\n\nИш ёки вакансия эълон қилиш учун расмий иш берувчилар ботимизга ўтинг:",
        'btn_goto_client_bot': "🚀 Иш берувчи ботига ўтиш",

        # 1-Qadam: Shaxsiy ma'lumotlar
        'step1_gender_title': "1-ҚАДАМ: ШАХСИЙ МАЪЛУМОТЛАР\n\n1.1 Жинсингизни танланг:",
        'gender_male': "👨 Эркак",
        'gender_female': "👩 Аёл",
        'step1_name_title': "1.2 Исм ва Фамилиянгизни киритинг:\n<i>(Масалан: Али Валиев)</i>",
        'step1_age_title': "1.3 Ёшингизни киритинг:\n<i>(Фақат сон киритинг, масалан: 25)</i>",
        'step1_age_invalid': "⚠️ Илтимос, ёшингизни тўғри мусбат бутун сонда киритинг (масалан: 25):",
        'step1_phone_title': "1.4 Телефон рақамингизни юборинг ёки қуйидаги форматда киритинг (+998901234567):",
        'btn_send_phone': "📱 Телефон рақамни улашиш",
        'step1_phone_invalid': "⚠️ Телефон рақами нотўғри. Илтимос, тугмани босинг ёки +998XXXXXXXXX форматида киритинг:",

        # 2-Qadam: Manzil va Joylashuv
        'step2_geo_title': "2-ҚАДАМ: МАНЗИЛ ВА ЖОЙЛАШУВ\n\n2.1 GPS Локациянгизни юборинг:\n<i>(Тизим автоматик вилоят ва туманни аниқлайди)</i>",
        'btn_send_gps': "📍 Локацияни юбориш",
        'btn_manual_region': "🏛 Вилоятни қўлда танлаш",
        'step2_address_title': "2.2 Аниқ манзилингизни киритинг:\n<i>(Маҳалла / Кўча ва Уй/хонадон рақами)</i>",
        'choose_region_worker': "📍 Қайси ҳудудда иш қидирмоқчисиз?\nВилоятни танланг:",

        # 3-Qadam: Kasb va Xizmat yo'nalishlari
        'choose_category': "3-ҚАДАМ: КАСБ ВА ХИЗМАТ ЙЎНАЛИШЛАРИ\n\n3.1 Асосий соҳани танланг:\n(Саҳифа {current}/{total})",
        'choose_position': "3.2 Мутахассисликларни танланг (10 тагача танлаш мумкин):\n(Саҳифа {current}/{total})\n\nТанланганлар: {selected_count}/10 та",
        'max_pos_alert': "⚠️ Сиз максимал 10 та мутахассислик танлашингиз мумкин!",
        'btn_continue': "➡️ Кейинги қадамга ўтиш ({count} та)",
        'btn_choose_other_cats': "➕ Бошқа соҳалардан ҳам танлаш",
        'btn_back_to_cats': "📂 Соҳалар рўйхатига қайтиш",
        'btn_back': "⬅️ Орқага",

        # 4-Qadam: Ish rejimi va Shartlari
        'step4_emp_type_title': "4-ҚАДАМ: ИШ РЕЖИМИ ВА ШАРТЛАРИ\n\n4.1 Қайси бандлик турида ишламоқчисиз?",
        'emp_type_daily': "⚡️ Бир марталик / Кунбай",
        'emp_type_permanent': "💼 Доимий иш",
        'emp_type_both': "🔄 Иккаласи ҳам",
        'step4_schedule_title': "4.2 Иш вақти режимини танланг:",
        'schedule_day': "☀️ 09:00 - 18:00 (Кундузги)",
        'schedule_24_7': "🚨 24/7 (Исталган вақтда / Шошилинч)",
        'schedule_flexible': "⏱ Эркин график",

        # 5-Qadam: Profilni tasdiqlash
        'step5_review_title': "📋 <b>5-ҚАДАМ: ПРОФИЛНИ ТАСДИҚЛАШ</b>\n\nИлтимос, киритилган маълумотларни текширинг:\n\n👤 <b>Ф.И:</b> {name} ({gender}, {age} ёш)\n📞 <b>Тел:</b> {phone}\n📍 <b>Ҳудуд:</b> {region}, {district}\n🏠 <b>Аниқ манзил:</b> {street_address}\n🛠 <b>Танланган соҳалар ва мутахассисликлар ({pos_count} та):</b>\n{positions}\n💼 <b>Бандлик тури:</b> {emp_type}\n⏱ <b>Иш режими:</b> {work_schedule}\n\nМаълумотлар тўғрими?",
        'btn_confirm_profile': "✅ Тасдиқлаш",
        'btn_restart_profile': "🔄 Қайтадан киритиш",
        'reg_success': "✅ Табриклаймиз! Сизнинг анкетангиз муваффақиятли сақланди ва профилингиз фаоллаштирилди.",

        # ASOSIY MENYU TUZILISHI
        'main_menu': "🏠 <b>24/7-ишлар — Асосий меню</b>\n\n👤 <b>Уста:</b> {name}\n📍 <b>Ҳудуд:</b> {location}\n🛠 <b>Соҳалар:</b> {positions}\n{status_badge}\n\nҚуйидаги бўлимлардан бирини танланг:",
        'status_active_badge': "🟢 <b>Ҳолат:</b> Фаол (Буюртмалар қабул қилинмоқда)",
        'status_busy_badge': "🔴 <b>Ҳолат:</b> Банд (Янги ишлар тўхтатилган)",
        
        # 1. ISHLARNI KO'RISH / QIDIRISH
        'btn_menu_jobs': "🔎 ИШЛАРНИ КЎРИШ / ҚИДИРИШ",
        'jobs_menu_title': "🔎 <b>ИШЛАРНИ ҚИДИРИШ ВА КЎРИШ</b>\n\nҚандай усулда иш қидирмоқчисиз?",
        'btn_jobs_matched': "📋 Барча ишлар",
        'btn_jobs_by_cat': "🔍 Категория бўйича излаш",
        'btn_jobs_by_geo': "🗺 Ҳудуд бўйича излаш",
        'jobs_empty': "🔍 Ҳозирда сизнинг мезонларингиз бўйича янги буюртмалар йўқ.\n\n🔔 Янги эълон қўшилиши билан сизга билдиришнома юборилади!",
        'job_card_text': "📄 <b>Эълон #{id} ({current}/{total}):</b>\n\n📋 <b>{category} / {service_type}</b>\n📍 <b>Манзил:</b> {address}\n⏱ <b>Вақт:</b> {work_time} ({work_format})\n💰 <b>Ҳақ:</b> {price}\n📝 <b>Тавсиф:</b> {desc}\n\n📞 <b>Иш берувчи:</b> {customer_name}",
        'btn_take_job': "💼 Ишни олиш",
        'btn_check_job_status': "🔍 Фаоллигини текшириш",
        'btn_refresh_jobs': "🔄 Саҳифани янгилаш",
        'btn_cancel': "❌ Бекор қилиш",
        'btn_contact_employer': "📞 Иш берувчи билан боғланиш",
        'btn_next_job': "➡️ Кейинги ({current}/{total})",
        'btn_prev_job': "⬅️ Олдинги ({current}/{total})",
        'btn_geo_district': "🏛 Фақат ўз туманим",
        'btn_geo_region': "📍 Бутун вилоят",
        'btn_geo_radius_5': "🎯 Радиус 5 км",
        'btn_geo_radius_10': "🎯 Радиус 10 км",
        'btn_geo_radius_25': "🎯 Радиус 25 км",

        # 2. MENING PROFILIM (KABINET)
        'btn_menu_profile': "👤 МЕНИНГ ПРОФИЛИМ (КАБИНЕТ)",
        'cabinet_title': "👤 <b>УСТА ПРОФИЛИ КАБИНЕТИ:</b>\n\n👤 <b>Ф.И.Ш:</b> {name} ({age} ёш, {gender})\n📞 <b>Тел:</b> {phone}\n📍 <b>Жойлашув:</b> {region}, {district}\n🏠 <b>Аниқ манзил:</b> {street_address}\n🛠 <b>Соҳалар ({pos_count}/10):</b>\n{positions}\n⏱ <b>Режим:</b> {work_schedule} | {emp_type}\n{status_badge}\n⭐️ <b>Рейтинг:</b> {rating} / 5.0 ({reviews_count} та шарҳ)\n✅ <b>Бажарилган ишлар:</b> {completed_count} та",
        'btn_edit_profile': "✏️ Маълумотларни таҳрирлаш",
        'btn_portfolio': "🖼 Иш намуналарим (Портфолио)",
        'edit_menu_title': "✏️ <b>Қайси маълумотингизни ўзгартирмоқчисиз?</b>",
        'btn_edit_name_age': "👤 Ф.И.Ш ва Ёшни ўзгартириш",
        'btn_edit_phone': "📞 Телефон рақамни янгилаш",
        'btn_edit_location': "📍 Манзил / Локацияни қайта юбориш",
        'btn_edit_positions': "🛠 Мутахассисликларни таҳрирлаш",
        
        # Portfolio
        'portfolio_title': "🖼 <b>ИШ НАМУНАЛАРИНГИЗ (ПОРТФОЛИО):</b>\n\nЮкланган ишлар сони: <b>{count}/5 та</b>\n\nУшбу намуналар буюртмачи ва мижозларга сизнинг маҳоратингизни кўрсатиш учун хизмат қилади.",
        'btn_add_portfolio_item': "➕ Янги намуна қўшиш",
        'btn_view_portfolio_items': "👀 Намуналаримни кўриш ({count} та)",
        'prompt_upload_portfolio_photo': "📸 <b>Янги намуна қўшиш (1/2):</b>\n\nИлтимос, бажарган ишингиз расмини юборинг:",
        'prompt_upload_portfolio_caption': "📝 <b>Янги намуна қўшиш (2/2):</b>\n\nУшбу иш намунаси ҳақида қисқача изоҳ/тавсиф ёзиб юборинг:",
        'prompt_edit_caption': "✏️ <b>Изоҳни таҳрирлаш:</b>\n\nУшбу намуна учун янги изоҳ матнини ёзиб юборинг:",
        'prompt_replace_photo': "🔄 <b>Расмни алмаштириш:</b>\n\nУшбу намуна учун янги расмни юборинг:",
        'portfolio_item_card': "📸 <b>ИШ НАМУНАСИ</b>\n📌 <b>{current} / {total} - намуна</b>\n\n📝 <b>Изоҳ:</b> {caption}",
        'portfolio_item_no_caption': "Киритилмаган",
        'btn_prev_item': "⬅️ Олдинги",
        'btn_next_item': "Кейинги ➡️",
        'btn_edit_caption': "✏️ Изоҳни таҳрирлаш",
        'btn_replace_photo': "🔄 Расмни алмаштириш",
        'btn_delete_item': "🗑 Ушбу намунани ўчириш",
        'btn_back_to_portfolio': "🖼 Портфолиога қайтиш",
        'photo_uploaded_success': "✅ Янги иш намунаси муваффақиятли қўшилди! ({count}/5 та)",
        'photo_replaced_success': "✅ Намуна расми муваффақиятли алмаштирилди!",
        'caption_updated_success': "✅ Намуна изоҳи муваффақиятли янгиланди!",
        'photo_deleted_success': "🗑 Намуна муваффақиятли ўчирилди.",
        'portfolio_full': "⚠️ Сиз максимал 5 та портфолио намунаси юклашингиз мумкин.",
        'portfolio_empty': "Сизда ҳали иш намуналари юкланмаган.",

        # 3. BANDLIK HOLATI (TOGGLE)
        'btn_menu_toggle_status': "🟢/🔴 БАНДЛИК ҲОЛАТИ",
        'status_active_msg': "🟢 <b>Сиз ҳозир ФАОЛ ҳолатдасиз!</b>\n\nЯнги буюртмалар ва мижозлар сиз билан бемалол боғлана олади.",
        'btn_set_busy': "🔴 Банд режимига ўтиш",
        'status_busy_msg': "🔴 <b>Сиз БАНД ҳолатдасиз!</b>\n\nТизим сизга вақтинча янги буюртмалар юбормайди.",
        'btn_set_active': "🟢 Фаол режимга ўтиш",

        # 4. REYTING VA SHARHLAR
        'btn_menu_reviews': "⭐️ МЕНИНГ БАҲОЛАРИМ ВА ШАРҲЛАР",
        'reviews_title': "⭐️ <b>РЕЙТИНГ ВА ШАРҲЛАР ҲИСОБОТИ:</b>\n\n⭐️ <b>Ўртача балл:</b> {rating} / 5.0 ({reviews_count} та баҳо)\n✅ <b>Муваффақиятли бажарилган ишлар:</b> {completed_count} та\n\n💬 <b>Мижозлар қолдирган сўнгги шарҳлар:</b>",
        'reviews_empty': "Ҳозирча шарҳлар мавжуд эмас.",
        'review_item': "💬 <b>{client_name}</b> ({rating} ⭐️):\n<i>\"{comment}\"</i>\n🕒 {date}\n",

        # 4.5. JAVOBLAR (YUBORILGAN SO'ROVLAR)
        'btn_menu_applications': "Жавоблар",
        'my_applications_title': "👥 <b>ЮБОРИЛГАН СЎРОВЛАР / ЖАВОБЛАР ({count} та):</b>\n\nҚуйидаги эълонларга сиз ўз таклифингизни юборгансиз:\n<i>(Саҳифа {current}/{total})</i>",
        'my_applications_empty': "📬 <b>Ҳозирча сиз ҳеч қандай ишга сўров юбормагансиз.</b>\n\n'Ишларни кўриш' бўлимига ўтиб ўзингизга мос ишларга таклиф юборишингиз мумкин!",
        'my_app_detail_card': (
            "📋 <b>ЮБОРИЛГАН СЎРОВ МАЪЛУМОТИ</b>\n"
            "📢 <b>Эълон:</b> #{job_id} — {job_title}\n"
            "📊 <b>Ҳолат:</b> {status_label}\n"
            "🕒 <b>Юборилган вақт:</b> {applied_at}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📍 <b>Иш манзили:</b> {address}\n"
            "💰 <b>Иш ҳақи:</b> {price}\n"
            "⏱ <b>Вақт / Формат:</b> {work_time} ({work_format})\n"
            "📝 <b>Иш тавсифи:</b> {desc}\n\n"
            "✉️ <b>Сиз юборган таклиф / хабар:</b>\n<i>\"{proposal_msg}\"</i>"
            "{contact_section}"
        ),
        'btn_view_application': "👥 Жавобни кўриш",
        'btn_delete_application': "🗑 Ўчириш",
        'btn_accept_invited_job': "💼 Ишни қабул қилиш / Таклиф юбориш",
        'app_deleted_success': "🗑 Ушбу иш сўровларингиз рўйхатидан олиб ташланди.",
        'btn_menu_update_gps': "📍 GPSни янгилаш",
        'prompt_send_gps_update': "📍 <b>GPS ЖОЙЛАШУВНИ ЯНГИЛАШ:</b>\n\nИлтимос, янги жойлашувингизни (GPS локация) юборинг.\nТизим сизга яқин масофадаги (5 км гача бўлган) ва ҳудудингиздаги барча янги эълонларни етказади:",
        'gps_updated_success': "✅ <b>GPS жойлашувингиз муваффақиятли янгиланди!</b>\n\n📍 <b>Ҳудуд:</b> {region}, {district}\n🌐 <b>Координата:</b> {gps}\n\nЭнди сизга яқин атрофда жойланган барча янги иш буюртмалари автоматик тарзда етказилади.",

        # 5. SOZLAMALAR
        'btn_menu_settings': "⚙️ СОЗЛАМАЛАР",
        'settings_title': "⚙️ <b>СОЗЛАМАЛАР БЎЛИМИ:</b>\n\nКеракли параметрни танланг:",
        'btn_settings_lang': "🌐 Тилни ўзгартириш",
        'btn_settings_notif': "🔔 Билдиришномалар",
        'notif_title': "🔔 <b>Билдиришнома режимини танланг:</b>\nҲозирги ҳолат: <b>{current}</b>",
        'notif_opt_all': "🔔 Барча хабарлар ёқиқ",
        'notif_opt_night': "🌙 Тунги режим (22:00 дан keyin овозсиз)",
        'notif_opt_off': "🔕 Билдиришномаларни бутунлай ўчириш",
        'notif_saved': "✅ Билдиришнома созламаси сақланди!",

        # 6. QO'LLAB-QUVVATLASH
        'btn_menu_support': "📞 ҚЎЛЛАБ-ҚУВВАТЛАШ",
        'support_title': "📞 <b>ҚЎЛЛАБ-ҚУВВАТЛАШ ВА ЁРДАМ:</b>\n\n📞 <b>Call-марказ:</b> {phone}\n⏰ <b>Иш вақти:</b> 09:00 дан 18:00 гача",
        'btn_write_admin': "👨‍💻 Администраторга ёзиш",
        'btn_guide': "📖 Фойдаланиш қўлланмаси",
        'guide_text': (
            "📖 <b>{project_name} БОТИДАН ФОЙДАЛАНИШ ҚЎЛЛАНМАСИ</b>\n\n"
            "Ушбу бот орқали сиз ўз соҳангиз бўйича янги иш буюртмаларини топишингиз, мижозлар билан тўғридан-тўғри боғланишингиз ва шахсий профилингизни бошқаришингиз мумкин.\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔘 <b>АСОСИЙ БЎЛИМЛАР ВА УЛАРНИНГ ВАЗИФАСИ:</b>\n\n"
            "1️⃣ <b>🔎 ИШЛАРНИ КЎРИШ / ҚИДИРИШ:</b>\n"
            "• <b>🎯 Менга мос ишлар:</b> Сиз рўйхатдан ўтишда танлаган соҳа, лавозимлар (10 тагача) ва яшаш ҳудудингизга мос энг сўнгги буюртмалар.\n"
            "• <b>🔍 Категория бўйича:</b> Исталган соҳани танлаб, ўша соҳадаги мавжуд барча эълонларни кўриш.\n"
            "• <b>🗺 Географик жойлашув бўйича:</b> Ўз туманингиз, бутун вилоят ёки GPS локациянгиздан 5км, 10км, 25км радиусдаги ишларни саралаш.\n\n"
            "2️⃣ <b>👤 МЕНИНГ ПРОФИЛИМ (КАБИНЕТ):</b>\n"
            "• Шахсий маълумотларингиз (исм, ёш, телефон, манзил, соҳалар, иш жадвали)ни кўриш.\n"
            "• <b>✏️ Таҳрирлаш:</b> Маълумотлар ўзгарганда исм, телефон, GPS манзил ёки мутахассисликларни янгилаш.\n"
            "• <b>🖼 Портфолиоларим:</b> Бажарилган ишларингиздан 5 тагача сифатли расмлар юклаб, мижозларга намойиш этиш.\n\n"
            "3️⃣ <b>🟢/🔴 БАНДЛИК ҲОЛАТИ:</b>\n"
            "• <b>🟢 Фаол режим:</b> Сиз буюртмаларни қабул қилишга тайёрсиз. Мижозлар сизни қидирувда кўришади.\n"
            "• <b>🔴 Банд режим:</b> Агар ҳозир иш билан банд бўлсангиз ёки дам олаётган бўлсангиз, ушбу режимни ёқинг.\n\n"
            "4️⃣ <b>⭐️ РЕЙТИНГ ВА ШАРҲЛАР:</b>\n"
            "• Буюртмаларни бажарганингиздан сўнг мижозлар томонидан қолдирилган баҳолар ва фикр-мулоҳазаларни кузатиш.\n\n"
            "5️⃣ <b>⚙️ СОЗЛАМАЛАР:</b>\n"
            "• Мулоқот тилини ўзгартириш ва билдиришномаларни созлаш.\n\n"
            "6️⃣ <b>📞 ҚЎЛЛАБ-ҚУВВАТЛАШ:</b>\n"
            "• Оператор ёки администратор билан боғланиш, таклиф ва шикоятларни юбориш.\n\n"
            "💡 <i>Эслатма: Кўпроқ ва даромадли ишлар топиш учун профилингизни тўлиқ тўлдиринг ва портфолионгизга расмlar жойланг!</i>"
        ),
        'btn_leave_feedback': "💬 Таклиф / Шикоят қолдириш",
        'prompt_feedback': "✍️ Илтимос, ўз таклиф ёки шикоятингизни ёзиб юборинг:",
        'feedback_received': "✅ Раҳмат! Сизнинг хабарингиз администраторга юборилди.",

        # Umumiy tugmalar va Xatolik / Fallback
        'btn_back_main': "⬅️ Асосий менюга қайтиш",
        'btn_goto_main_menu': "🏠 Бош саҳифага қайтиш",
        'btn_restart_bot': "🔄 Ботни қайта ишга тушириш (/start)",
        'btn_back': "⬅️ Орқага",
        'bot_error_msg': "⚠️ <b>Кечирасиз, тизимда носозлик юз берди!</b>\n\nБотни қайтадан тўлиқ ишга тушириш учун қуйидаги буйруқни босинг:\n\n👉 <b>/start</b>",
        'bot_outdated_button_msg': "🔄 <b>Тизим янгиланди / сессия эскирган</b>\n\nДавом этиш ва ботни янгилаш учун қуйидаги буйруқни босинг:\n\n👉 <b>/start</b>",
        'bot_restarted_notification': "🚀 <b>{project_name} боти янгиланди!</b>\n\n⚙️ Тизимда янгиланишлар амалга оширилди ва барча хизматлар барқарор ишламоқда.\n\nБотдан фойдаланишни давом эттириш учун босинг:\n👉 <b>/start</b>",
        'job_status_active_alert': "✅ Ушбу эълон айни пайтда ФАОЛ ва қабул қилиш учун очиқ!",
        'job_status_taken_alert': "⚠️ Кечирасиз, ушбу иш бошқа мутахассис томонидан олинган ёки бириктирилган!",
        'job_status_closed_alert': "❌ Ушбу иш эълони иш берувчи томонидан олиб ташланган ёки ёпилган!",
        'job_already_applied_alert': "ℹ️ Сиз аллақачон ушбу иш бўйича сўров юборгансиз. Иш берувчи жавобини кутинг!",
        'prompt_apply_message': "✍️ <b>Иш берувчига таклиф / хабар юбориш:</b>\n\nЭълон: <b>#{job_id} — {title}</b>\n\nИш берувчига ўзингиз ҳақингизда қисқача маълумот, нарх ёки қачон етиб бора олишингиз ҳақида хабар ёзиб юборинг:\n<i>(Масалан: Ассалому алайкум, мен 5 йиллик тажрибали устаман, 30 дақиқада етиб бораман)</i>",
        'apply_confirm_title': "📋 <b>СЎРОВНИ ТАСДИҚЛАШ:</b>\n\n📢 <b>Эълон:</b> #{job_id} — {title}\n✉️ <b>Сизнинг хабарингиз:</b>\n<i>\"{msg}\"</i>\n\nИш берувчига юборилсинми?",
        'btn_send_proposal': "🚀 Юбориш",
        'btn_edit_proposal': "✏️ Ўзгартириш",
        'btn_cancel_proposal': "❌ Бекор қилиш",
        'apply_success_msg': "🎉 <b>Сўровингиз иш берувчига муваффақиятли юборилди!</b>\n\nИш берувчи хабарингизни кўриб чиқиб сиз билан боғланади ёки жавоб қайтаради. Илтимос, жавоб келишини кутинг.",
    },
    'ru': {
        'choose_lang': "Здравствуйте! Пожалуйста, выберите язык:",
        'lang_selected': "🇷🇺 Выбран русский язык.",
        'welcome_back': "Здравствуйте, <b>{name}</b>! 👋\n\nДобро пожаловать в платформу <b>{project_name}</b>!\nВыберите нужный раздел из меню ниже:",
        
        # 0.1-Qadam: Rol
        'choose_role': "Выберите один из вариантов:",
        'role_worker': "🛠 Ищу работу / Войти как специалист",
        'role_client': "📢 Ищу работников / Разместить вакансию",
        'client_redirect_msg': "🚀 <b>Бот работодателей</b>\n\nДля размещения работы перейдите в бот для работодателей:",
        'btn_goto_client_bot': "🚀 Перейти в бот работодателей",

        # 1-Qadam: Shaxsiy ma'lumotlar
        'step1_gender_title': "ШАГ 1: ЛИЧНЫЕ ДАННЫЕ\n\n1.1 Выберите ваш пол:",
        'gender_male': "👨 Мужской",
        'gender_female': "👩 Женский",
        'step1_name_title': "1.2 Введите ваше Имя и Фамилию:\n<i>(Например: Али Валиев)</i>",
        'step1_age_title': "1.3 Укажите ваш возраст:\n<i>(Только число, например: 25)</i>",
        'step1_age_invalid': "⚠️ Пожалуйста, введите корректный возраст (например: 25):",
        'step1_phone_title': "1.4 Отправьте или введите номер телефона (+998901234567):",
        'btn_send_phone': "📱 Поделиться номером",
        'step1_phone_invalid': "⚠️ Неверный номер телефона! Введите в формате +998XXXXXXXXX:",

        # 2-Qadam: Manzil va Joylashuv
        'step2_geo_title': "ШАГ 2: АДРЕС И МЕСТОПОЛОЖЕНИЕ\n\n2.1 Отправьте GPS локацию:",
        'btn_send_gps': "📍 Отправить локацию",
        'btn_manual_region': "🏛 Выбрать область вручную",
        'step2_address_title': "2.2 Введите точный адрес:\n<i>(Махалля / Улица и номер дома)</i>",
        'choose_region_worker': "📍 В каком регионе вы ищете работу?\nВыберите область:",

        # 3-Qadam: Kasb va Xizmat yo'nalishlari
        'choose_category': "ШАГ 3: ПРОФЕССИЯ И СФЕРЫ ДЕЯТЕЛЬНОСТИ\n\n3.1 Выберите сферу:\n(Страница {current}/{total})",
        'choose_position': "3.2 Выберите специальности (до 10 позиций):\n(Страница {current}/{total})\n\nВыбрано: {selected_count}/10",
        'max_pos_alert': "⚠️ Вы можете выбрать максимум 10 специальностей!",
        'btn_continue': "➡️ Перейти к следующему шагу ({count})",
        'btn_choose_other_cats': "➕ Выбрать из других сфер",
        'btn_back_to_cats': "📂 Вернуться к списку категорий",
        'btn_back': "⬅️ Назад",

        # 4-Qadam: Ish rejimi va Shartlari
        'step4_emp_type_title': "ШАГ 4: ГРАФИК И УСЛОВИЯ РАБОТЫ\n\n4.1 Какой формат занятости вас интересует?",
        'emp_type_daily': "⚡️ Разовая / Посуточная",
        'emp_type_permanent': "💼 Постоянная работа",
        'emp_type_both': "🔄 Оба варианта",
        'step4_schedule_title': "4.2 Выберите график работы:",
        'schedule_day': "☀️ 09:00 - 18:00 (Дневной)",
        'schedule_24_7': "🚨 24/7 (В любое время / Срочный)",
        'schedule_flexible': "⏱ Свободный график",

        # 5-Qadam: Profilni tasdiqlash
        'step5_review_title': "📋 <b>ШАГ 5: ПОДТВЕРЖДЕНИЕ ПРОФИЛЯ</b>\n\nПожалуйста, проверьте данные:\n\n👤 <b>Ф.И:</b> {name} ({gender}, {age} лет)\n📞 <b>Тел:</b> {phone}\n📍 <b>Регион:</b> {region}, {district}\n🏠 <b>Точный адрес:</b> {street_address}\n🛠 <b>Выбранные специальности ({pos_count}):</b>\n{positions}\n💼 <b>Тип занятости:</b> {emp_type}\n⏱ <b>График:</b> {work_schedule}\n\nДанные верны?",
        'btn_confirm_profile': "✅ Подтвердить",
        'btn_restart_profile': "🔄 Ввести заново",
        'reg_success': "✅ Поздравляем! Ваша анкета успешно сохранена.",

        # ASOSIY MENYU TUZILISHI
        'main_menu': "🏠 <b>{project_name} — Главное меню</b>\n\n👤 <b>Специалист:</b> {name}\n📍 <b>Регион:</b> {location}\n🛠 <b>Специальности:</b> {positions}\n{status_badge}\n\nВыберите нужный раздел:",
        'status_active_badge': "🟢 <b>Статус:</b> Активен (Заказы принимаются)",
        'status_busy_badge': "🔴 <b>Статус:</b> Занят (Новые заказы приостановлены)",
        
        # 1. ISHLARNI KO'RISH / QIDIRISH
        'btn_menu_jobs': "🔎 ПРОСМОТР / ПОИСК ЗАКАЗОВ",
        'jobs_menu_title': "🔎 <b>ПОИСК И ПРОСМОТР ЗАКАЗОВ</b>\n\nКак вы хотите искать работу?",
        'btn_jobs_matched': "📋 Все заказы",
        'btn_jobs_by_cat': "🔍 Поиск по категории",
        'btn_jobs_by_geo': "🗺 Поиск по геолокации",
        'jobs_empty': "🔍 В данный момент по вашим критериям нет новых заказов.",
        'btn_take_job': "💼 Взять заказ",
        'btn_check_job_status': "🔍 Проверить статус",
        'btn_refresh_jobs': "🔄 Обновить страницу",
        'btn_cancel': "❌ Отмена",
        'btn_contact_employer': "📞 Связаться с заказчиком",
        'btn_next_job': "➡️ Следующий ({current}/{total})",
        'btn_prev_job': "⬅️ Предыдущий ({current}/{total})",
        'btn_geo_district': "🏛 Только мой район",
        'btn_geo_region': "📍 Вся область",
        'btn_geo_radius_5': "🎯 Радиус 5 км",
        'btn_geo_radius_10': "🎯 Радиус 10 км",
        'btn_geo_radius_25': "🎯 Радиус 25 км",

        # 2. MENING PROFILIM (KABINET)
        'btn_menu_profile': "👤 МОЙ ПРОФИЛЬ (КАБИНЕТ)",
        'cabinet_title': "👤 <b>КАБИНЕТ МАСТЕРА:</b>\n\n👤 <b>Ф.И.О:</b> {name} ({age} лет, {gender})\n📞 <b>Тел:</b> {phone}\n📍 <b>Локация:</b> {region}, {district}\n🏠 <b>Адрес:</b> {street_address}\n🛠 <b>Специальности ({pos_count}/10):</b>\n{positions}\n⏱ <b>График:</b> {work_schedule} | {emp_type}\n{status_badge}\n⭐️ <b>Рейтинг:</b> {rating} / 5.0 ({reviews_count} отзывов)\n✅ <b>Выполнено заказов:</b> {completed_count}",
        'btn_edit_profile': "✏️ Редактировать профиль",
        'btn_portfolio': "🖼 Портфолио работ",
        'edit_menu_title': "✏️ <b>Что вы хотите изменить?</b>",
        'btn_edit_name_age': "👤 Изменить Ф.И.О и возраст",
        'btn_edit_phone': "📞 Изменить номер телефона",
        'btn_edit_location': "📍 Обновить адрес / локацию",
        'btn_edit_positions': "🛠 Изменить специальности",
        
        # Portfolio
        'portfolio_title': "🖼 <b>ВАШЕ ПОРТФОЛИО:</b>\n\nЗагружено работ: <b>{count}/5</b>",
        'btn_add_portfolio_item': "➕ Добавить образец",
        'btn_view_portfolio_items': "👀 Мои образцы ({count})",
        'prompt_upload_portfolio_photo': "📸 <b>Добавление работы (1/2):</b>\n\nОтправьте фото выполненной работы:",
        'prompt_upload_portfolio_caption': "📝 <b>Добавление работы (2/2):</b>\n\nНапишите краткое описание этой работы:",
        'prompt_edit_caption': "✏️ <b>Редактирование описания:</b>",
        'prompt_replace_photo': "🔄 <b>Замена фотографии:</b>",
        'portfolio_item_card': "📸 <b>ОБРАЗЕЦ РАБОТЫ</b>\n📌 <b>{current} / {total}</b>\n\n📝 <b>Описание:</b> {caption}",
        'portfolio_item_no_caption': "Без описания",
        'btn_prev_item': "⬅️ Назад",
        'btn_next_item': "➡️ Вперед",
        'btn_edit_caption': "✏️ Изменить текст",
        'btn_replace_photo': "🔄 Заменить фото",
        'btn_delete_item': "🗑 Удалить",
        'btn_back_to_portfolio': "⬅️ Назад в меню портфолио",
        'portfolio_empty': "У вас пока нет образцов работ.",
        'portfolio_item_deleted': "🗑 Образец удален.",
        'portfolio_caption_updated': "✅ Описание обновлено!",
        'portfolio_photo_updated': "✅ Фотография заменена!",
        'portfolio_max_reached': "⚠️ Максимум 5 образцов работ!",
        'portfolio_item_saved': "🎉 Образец работы успешно сохранен!",

        # 3. BANDLIK HOLATI
        'btn_menu_toggle_status': "🟢/🔴 СТАТУС ЗАНЯТОСТИ",
        'btn_menu_status': "🟢/🔴 СТАТУС ЗАНЯТОСТИ",
        'status_active_msg': "🟢 <b>Вы сейчас в АКТИВНОМ статусе!</b>\n\nНовые заказы и клиенты могут связываться с вами, и вы будете получать уведомления о новых заявках.",
        'btn_set_busy': "🔴 Включить режим 'Занят'",
        'status_busy_msg': "🔴 <b>Вы в режиме 'ЗАНЯТ'!</b>\n\nСистема временно не будет отправлять вам новые заказы, и ваш профиль будет отображаться как занятый.",
        'btn_set_active': "🟢 Включить режим 'Активен'",

        # 4. REYTING VA SHARHLAR
        'btn_menu_reviews': "⭐️ МОИ ОЦЕНКИ И ОТЗЫВЫ",
        'reviews_title': "⭐️ <b>ОТЧЕТ ПО ОЦЕНКАМ И ОТЗЫВАМ:</b>\n\n⭐️ <b>Средний балл:</b> {rating} / 5.0 ({reviews_count} оценок)\n✅ <b>Выполнено заказов:</b> {completed_count}",
        'reviews_empty': "Отзывов пока нет.",
        'review_item': "💬 <b>{client_name}</b> ({rating} ⭐️):\n<i>\"{comment}\"</i>\n🕒 {date}\n",

        # 4.5. JAVOBLAR (YUBORILGAN SO'ROVLAR)
        'btn_menu_applications': "Отклики",
        'my_applications_title': "👥 <b>ОТПРАВЛЕННЫЕ ОТКЛИКИ ({count}):</b>\n\nСписок объявлений, на которые вы подали заявку:\n<i>(Страница {current}/{total})</i>",
        'my_applications_empty': "📬 <b>Вы пока не отправляли отклики на заказы.</b>\n\nПерейдите в раздел 'Просмотр заказов', чтобы отправить предложения заказчикам!",
        'my_app_detail_card': (
            "📋 <b>ИНФОРМАЦИЯ ОБ ОТКЛИКЕ</b>\n"
            "📢 <b>Заказ:</b> #{job_id} — {job_title}\n"
            "📊 <b>Статус:</b> {status_label}\n"
            "🕒 <b>Дата подачи:</b> {applied_at}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📍 <b>Адрес:</b> {address}\n"
            "💰 <b>Оплата:</b> {price}\n"
            "⏱ <b>Время / Формат:</b> {work_time} ({work_format})\n"
            "📝 <b>Описание работы:</b> {desc}\n\n"
            "✉️ <b>Ваше предложение / сообщение:</b>\n<i>\"{proposal_msg}\"</i>"
            "{contact_section}"
        ),
        'btn_view_application': "👥 Посмотреть отклик",
        'btn_delete_application': "🗑 Удалить",
        'btn_accept_invited_job': "💼 Принять заказ / Отправить отклик",
        'app_deleted_success': "🗑 Заказ успешно удален из вашего списка откликов.",
        'btn_menu_update_gps': "📍 Обновить GPS",
        'prompt_send_gps_update': "📍 <b>ОБНОВЛЕНИЕ GPS МЕСТОПОЛОЖЕНИЯ:</b>\n\nПожалуйста, отправьте ваше текущее местоположение (GPS).\nСистема будет отправлять вам все новые заказы в радиусе 5 км и в вашем регионе:",
        'gps_updated_success': "✅ <b>Ваше GPS местоположение успешно обновлено!</b>\n\n📍 <b>Регион:</b> {region}, {district}\n🌐 <b>Координаты:</b> {gps}\n\nТеперь вам будут автоматически приходить все новые заказы поблизости.",

        # 5. SOZLAMALAR
        'btn_menu_settings': "⚙️ НАСТРОЙКИ",
        'settings_title': "⚙️ <b>РАЗДЕЛ НАСТРОЕК:</b>",
        'btn_settings_lang': "🌐 Сменить язык",
        'btn_settings_notif': "🔔 Уведомления",
        'notif_title': "🔔 <b>Режим уведомлений:</b>\nТекущий: <b>{current}</b>",
        'notif_opt_all': "🔔 Все уведомления",
        'notif_opt_night': "🌙 Ночной режим",
        'notif_opt_off': "🔕 Выключить",
        'notif_saved': "✅ Настройки сохранены!",

        # 6. QO'LLAB-QUVVATLASH
        'btn_menu_support': "📞 ПОДДЕРЖКА",
        'support_title': "📞 <b>ПОДДЕРЖКА И ПОМОЩЬ:</b>\n\n📞 <b>Колл-центр:</b> {phone}\n⏰ <b>Время работы:</b> 09:00 - 18:00",
        'btn_write_admin': "👨‍💻 Связаться с админом",
        'btn_guide': "📖 Инструкция",
        'guide_text': "📖 <b>РУКОВОДСТВО ПО ИСПОЛЬЗОВАНИЮ {project_name}</b>",
        'btn_leave_feedback': "💬 Оставить отзыв / жалобу",
        'prompt_feedback': "✍️ Пожалуйста, напишите ваше сообщение:",
        'feedback_received': "✅ Спасибо! Сообщение отправлено администрации.",

        # Umumiy tugmalar va Xatolik / Fallback
        'btn_back_main': "⬅️ Вернуться в главное меню",
        'btn_goto_main_menu': "🏠 Перейти на главную страницу",
        'btn_restart_bot': "🔄 Перезапустить бота (/start)",
        'btn_back': "⬅️ Назад",
        'bot_error_msg': "⚠️ <b>Извините, произошел сбой в системе!</b>\n\nЧтобы перезапустить бота, нажмите на команду:\n\n👉 <b>/start</b>",
        'bot_outdated_button_msg': "🔄 <b>Система обновлена / сессия устарела</b>\n\nЧтобы продолжить и обновить бота, нажмите:\n\n👉 <b>/start</b>",
        'bot_restarted_notification': "🚀 <b>Бот {project_name} обновлен!</b>\n\n⚙️ Были установлены системные обновления, и все сервисы работают стабильно.\n\nЧтобы продолжить работу с ботом, нажмите:\n👉 <b>/start</b>",
        'job_card_text': "📄 <b>Объявление #{id} ({current}/{total}):</b>\n\n📋 <b>{category} / {service_type}</b>\n📍 <b>Адрес:</b> {address}\n⏱ <b>Время:</b> {work_time} ({work_format})\n💰 <b>Оплата:</b> {price}\n📝 <b>Описание:</b> {desc}\n\n📞 <b>Работодатель:</b> {customer_name}",
        'job_status_active_alert': "✅ Это объявление АКТИВНО и доступно для отклика!",
        'job_status_taken_alert': "⚠️ Извините, данный заказ уже взят другим специалистом!",
        'job_status_closed_alert': "❌ Это объявление снято работодателем или закрыто!",
        'job_already_applied_alert': "ℹ️ Вы уже отправили отклик на эту работу. Ожидайте ответа заказчика!",
        'prompt_apply_message': "✍️ <b>Отправить отклик / сообщение работодателю:</b>\n\nОбъявление: <b>#{job_id} — {title}</b>\n\nНапишите кратко о вашем опыте, цене или когда сможете прибыть:\n<i>(Например: Здравствуйте, опыт 5 лет, смогу прибыть через 30 минут)</i>",
        'apply_confirm_title': "📋 <b>ПОДТВЕРЖДЕНИЕ ОТКЛИКА:</b>\n\n📢 <b>Заказ:</b> #{job_id} — {title}\n✉️ <b>Ваше сообщение:</b>\n<i>\"{msg}\"</i>\n\nОтправить работодателю?",
        'btn_send_proposal': "🚀 Отправить",
        'btn_edit_proposal': "✏️ Изменить",
        'btn_cancel_proposal': "❌ Отменить",
        'apply_success_msg': "🎉 <b>Ваш отклик успешно отправлен работодателю!</b>\n\nРаботодатель рассмотрит его и свяжется с вами. Пожалуйста, ожидайте ответа.",
        'portfolio_full': "⚠️ В портфолио можно загрузить максимум 5 фотографий!",
        'photo_uploaded_success': "✅ Фото успешно добавлено в портфолио!",
        'photo_deleted_success': "🗑 Фото удалено из портфолио.",
        'caption_updated_success': "✅ Описание успешно обновлено!",
        'photo_replaced_success': "✅ Фото успешно заменено!",
    },
    'en': {
        'choose_lang': "Welcome! Please choose your preferred language:",
        'lang_selected': "🇬🇧 English language selected.",
        'welcome_back': "Welcome, <b>{name}</b>! 👋\n\nWelcome back to <b>{project_name}</b> platform!\nPlease select a section from the menu below:",
        
        # 0.1-Qadam: Rol
        'choose_role': "Please choose one of the options:",
        'role_worker': "🛠 Looking for jobs / Join as specialist",
        'role_client': "📢 Hiring workers / Post a job",
        'client_redirect_msg': "🚀 <b>Employer Bot</b>\n\nTo post vacancies and hire workers, switch to our official Employer Bot:",
        'btn_goto_client_bot': "🚀 Switch to Employer Bot",

        # 1-Qadam: Shaxsiy ma'lumotlar
        'step1_gender_title': "STEP 1: PERSONAL INFORMATION\n\n1.1 Select your gender:",
        'gender_male': "👨 Male",
        'gender_female': "👩 Female",
        'step1_name_title': "1.2 Enter your Full Name:\n<i>(e.g., John Doe)</i>",
        'step1_age_title': "1.3 Enter your age:\n<i>(Numbers only, e.g., 25)</i>",
        'step1_age_invalid': "⚠️ Please enter a valid positive number for age (e.g., 25):",
        'step1_phone_title': "1.4 Send or enter your phone number (+998901234567):",
        'btn_send_phone': "📱 Share phone number",
        'step1_phone_invalid': "⚠️ Invalid phone number! Please enter in +998XXXXXXXXX format:",

        # 2-Qadam: Manzil va Joylashuv
        'step2_geo_title': "STEP 2: LOCATION & ADDRESS\n\n2.1 Send your GPS location:\n<i>(System auto-detects region and district)</i>",
        'btn_send_gps': "📍 Send GPS Location",
        'btn_manual_region': "🏛 Select Region Manually",
        'step2_address_title': "2.2 Enter your exact street address / landmark:",
        'choose_region_worker': "📍 Where do you want to find work?\nSelect region:",

        # 3-Qadam: Kasb va Xizmat yo'nalishlari
        'choose_category': "STEP 3: SKILLS & CATEGORIES\n\n3.1 Select main industry:\n(Page {current}/{total})",
        'choose_position': "3.2 Select specialties (up to 10):\n(Page {current}/{total})\n\nSelected: {selected_count}/10",
        'max_pos_alert': "⚠️ You can select a maximum of 10 specialties!",
        'btn_continue': "➡️ Next Step ({count})",
        'btn_choose_other_cats': "➕ Select from other categories",
        'btn_back_to_cats': "📂 Back to Category List",
        'btn_back': "⬅️ Back",

        # 4-Qadam: Ish rejimi va Shartlari
        'step4_emp_type_title': "STEP 4: WORK FORMAT & SCHEDULE\n\n4.1 What work format do you prefer?",
        'emp_type_daily': "⚡️ One-time / Daily Gig",
        'emp_type_permanent': "💼 Full-time Job",
        'emp_type_both': "🔄 Both",
        'step4_schedule_title': "4.2 Select working schedule:",
        'schedule_day': "☀️ 09:00 - 18:00 (Day shift)",
        'schedule_24_7': "🚨 24/7 (Any time / Urgent)",
        'schedule_flexible': "⏱ Flexible Hours",

        # 5-Qadam: Profilni tasdiqlash
        'step5_review_title': "📋 <b>STEP 5: CONFIRM PROFILE</b>\n\nPlease check your details:\n\n👤 <b>Name:</b> {name} ({gender}, {age} y/o)\n📞 <b>Phone:</b> {phone}\n📍 <b>Location:</b> {region}, {district}\n🏠 <b>Address:</b> {street_address}\n🛠 <b>Specialties ({pos_count}):</b>\n{positions}\n💼 <b>Employment:</b> {emp_type}\n⏱ <b>Schedule:</b> {work_schedule}\n\nAre these details correct?",
        'btn_confirm_profile': "✅ Confirm & Activate",
        'btn_restart_profile': "🔄 Start Over",
        'reg_success': "✅ Congratulations! Your profile has been activated.",

        # ASOSIY MENYU TUZILISHI
        'main_menu': "🏠 <b>{project_name} — Main Menu</b>\n\n👤 <b>Specialist:</b> {name}\n📍 <b>Location:</b> {location}\n🛠 <b>Specialties:</b> {positions}\n{status_badge}\n\nSelect an option below:",
        'status_active_badge': "🟢 <b>Status:</b> Active (Ready for orders)",
        'status_busy_badge': "🔴 <b>Status:</b> Busy (Orders paused)",
        
        # 1. ISHLARNI KO'RISH / QIDIRISH
        'btn_menu_jobs': "🔎 VIEW & SEARCH JOBS",
        'jobs_menu_title': "🔎 <b>SEARCH & VIEW JOBS</b>\n\nHow would you like to search for jobs?",
        'btn_jobs_matched': "📋 All Jobs",
        'btn_jobs_by_cat': "🔍 Search by Category",
        'btn_jobs_by_geo': "🗺 Search by Location",
        'jobs_empty': "🔍 No new orders found matching your criteria currently.",
        'job_card_text': "📄 <b>Order #{id} ({current}/{total}):</b>\n\n📋 <b>{category} / {service_type}</b>\n📍 <b>Location:</b> {address}\n⏱ <b>Time:</b> {work_time} ({work_format})\n💰 <b>Payment:</b> {price}\n📝 <b>Description:</b> {desc}\n\n📞 <b>Employer:</b> {customer_name}",
        'btn_take_job': "💼 Take Job",
        'btn_check_job_status': "🔍 Check Status",
        'btn_refresh_jobs': "🔄 Refresh Page",
        'btn_cancel': "❌ Cancel",
        'btn_contact_employer': "📞 Contact Employer",
        'btn_next_job': "➡️ Next ({current}/{total})",
        'btn_prev_job': "⬅️ Previous ({current}/{total})",
        'btn_geo_district': "🏛 Only My District",
        'btn_geo_region': "📍 Entire Region",
        'btn_geo_radius_5': "🎯 Radius 5 km",
        'btn_geo_radius_10': "🎯 Radius 10 km",
        'btn_geo_radius_25': "🎯 Radius 25 km",

        # 2. MENING PROFILIM (KABINET)
        'btn_menu_profile': "👤 MY PROFILE (CABINET)",
        'cabinet_title': "👤 <b>SPECIALIST CABINET:</b>\n\n👤 <b>Full Name:</b> {name} ({age} y/o, {gender})\n📞 <b>Phone:</b> {phone}\n📍 <b>Location:</b> {region}, {district}\n🏠 <b>Address:</b> {street_address}\n🛠 <b>Specialties ({pos_count}/10):</b>\n{positions}\n⏱ <b>Schedule:</b> {work_schedule} | {emp_type}\n{status_badge}\n⭐️ <b>Rating:</b> {rating} / 5.0 ({reviews_count} reviews)\n✅ <b>Completed Jobs:</b> {completed_count}",
        'btn_edit_profile': "✏️ Edit Profile",
        'btn_portfolio': "🖼 Work Portfolio",
        'edit_menu_title': "✏️ <b>What would you like to edit?</b>",
        'btn_edit_name_age': "👤 Edit Name & Age",
        'btn_edit_phone': "📞 Update Phone Number",
        'btn_edit_location': "📍 Update Location / GPS",
        'btn_edit_positions': "🛠 Edit Specialties",
        
        # Portfolio
        'portfolio_title': "🖼 <b>YOUR PORTFOLIO:</b>\n\nUploaded items: <b>{count}/5</b>",
        'btn_add_portfolio_item': "➕ Add New Item",
        'btn_view_portfolio_items': "👀 View My Portfolio ({count})",
        'prompt_upload_portfolio_photo': "📸 <b>Add Portfolio Item (1/2):</b>\n\nPlease upload a photo of your work:",
        'prompt_upload_portfolio_caption': "📝 <b>Add Portfolio Item (2/2):</b>\n\nEnter a short description:",
        'prompt_edit_caption': "✏️ <b>Edit Description:</b>",
        'prompt_replace_photo': "🔄 <b>Replace Photo:</b>",
        'portfolio_item_card': "📸 <b>WORK SAMPLE</b>\n📌 <b>{current} / {total}</b>\n\n📝 <b>Description:</b> {caption}",
        'portfolio_item_no_caption': "No description",
        'btn_prev_item': "⬅️ Previous",
        'btn_next_item': "➡️ Next",
        'btn_edit_caption': "✏️ Edit Text",
        'btn_replace_photo': "🔄 Replace Photo",
        'btn_delete_item': "🗑 Delete",
        'btn_back_to_portfolio': "⬅️ Back to Portfolio",
        'portfolio_empty': "You have not uploaded any work samples yet.",
        'portfolio_item_deleted': "🗑 Sample deleted.",
        'portfolio_caption_updated': "✅ Description updated!",
        'portfolio_photo_updated': "✅ Photo replaced!",
        'portfolio_max_reached': "⚠️ Maximum 5 items allowed!",
        'portfolio_item_saved': "🎉 Portfolio item saved successfully!",

        # 3. BANDLIK HOLATI
        'btn_menu_toggle_status': "🟢/🔴 AVAILABILITY STATUS",
        'btn_menu_status': "🟢/🔴 AVAILABILITY STATUS",
        'status_active_msg': "🟢 <b>You are currently in ACTIVE status!</b>\n\nNew job orders and clients can reach you, and you will receive instant job alerts.",
        'btn_set_busy': "🔴 Switch to Busy",
        'status_busy_msg': "🔴 <b>You are currently BUSY!</b>\n\nThe system will temporarily pause sending you new job notifications.",
        'btn_set_active': "🟢 Switch to Active",

        # 4. REYTING VA SHARHLAR
        'btn_menu_reviews': "⭐️ MY RATINGS & REVIEWS",
        'reviews_title': "⭐️ <b>RATINGS & REVIEWS REPORT:</b>\n\n⭐️ <b>Average rating:</b> {rating} / 5.0 ({reviews_count} ratings)\n✅ <b>Completed jobs:</b> {completed_count}",
        'reviews_empty': "No reviews yet.",
        'review_item': "💬 <b>{client_name}</b> ({rating} ⭐️):\n<i>\"{comment}\"</i>\n🕒 {date}\n",

        # 4.5. JAVOBLAR (YUBORILGAN SO'ROVLAR)
        'btn_menu_applications': "Applications",
        'my_applications_title': "👥 <b>SENT APPLICATIONS / PROPOSALS ({count}):</b>\n\nJob listings you have applied to:\n<i>(Page {current}/{total})</i>",
        'my_applications_empty': "📬 <b>You haven't applied to any jobs yet.</b>\n\nGo to 'View & Search Jobs' to send proposals to clients!",
        'my_app_detail_card': (
            "📋 <b>APPLICATION DETAILS</b>\n"
            "📢 <b>Job:</b> #{job_id} — {job_title}\n"
            "📊 <b>Status:</b> {status_label}\n"
            "🕒 <b>Applied at:</b> {applied_at}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📍 <b>Location:</b> {address}\n"
            "💰 <b>Payment:</b> {price}\n"
            "⏱ <b>Time / Format:</b> {work_time} ({work_format})\n"
            "📝 <b>Description:</b> {desc}\n\n"
            "✉️ <b>Your Proposal Message:</b>\n<i>\"{proposal_msg}\"</i>"
            "{contact_section}"
        ),
        'btn_view_application': "👥 View Application",
        'btn_delete_application': "🗑 Delete",
        'btn_accept_invited_job': "💼 Accept Job / Send Proposal",
        'app_deleted_success': "🗑 Successfully removed from your applications.",
        'btn_menu_update_gps': "📍 Update GPS",
        'prompt_send_gps_update': "📍 <b>UPDATE GPS LOCATION:</b>\n\nPlease send your current GPS location.\nThe system will automatically deliver all new job orders within 5 km and in your area:",
        'gps_updated_success': "✅ <b>Your GPS location has been successfully updated!</b>\n\n📍 <b>Region:</b> {region}, {district}\n🌐 <b>Coordinates:</b> {gps}\n\nNow you will automatically receive all nearby new job notifications.",

        # 5. SOZLAMALAR
        'btn_menu_settings': "⚙️ SETTINGS",
        'settings_title': "⚙️ <b>SETTINGS:</b>",
        'btn_settings_lang': "🌐 Change Language",
        'btn_settings_notif': "🔔 Notifications",
        'notif_title': "🔔 <b>Select notification mode:</b>\nCurrent: <b>{current}</b>",
        'notif_opt_all': "🔔 All notifications on",
        'notif_opt_night': "🌙 Night mode",
        'notif_opt_off': "🔕 Turn off",
        'notif_saved': "✅ Settings saved!",

        # 6. QO'LLAB-QUVVATLASH
        'btn_menu_support': "📞 SUPPORT",
        'support_title': "📞 <b>SUPPORT & HELP:</b>\n\n📞 <b>Call center:</b> {phone}\n⏰ <b>Working hours:</b> 09:00 - 18:00",
        'btn_write_admin': "👨‍💻 Contact Admin",
        'btn_guide': "📖 User Guide",
        'guide_text': (
            "📖 <b>USER GUIDE FOR {project_name} BOT</b>\n\n"
            "This bot helps you find relevant job orders and vacancies in your field, contact clients directly, and manage your master profile.\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔘 <b>MAIN SECTIONS & THEIR FUNCTIONS:</b>\n\n"
            "1️⃣ <b>🔎 VIEW & SEARCH JOBS:</b>\n"
            "• <b>🎯 Matching Jobs:</b> Orders matching your selected industries, specialties (up to 10), and location.\n"
            "• <b>🔍 Search by Category:</b> Browse all available job postings by industry.\n"
            "• <b>🗺 Search by Location:</b> Filter orders in your district, whole region, or within 5km, 10km, 25km radius from your GPS.\n\n"
            "2️⃣ <b>👤 MY PROFILE (CABINET):</b>\n"
            "• View personal information (name, age, phone, location, specialties, work schedule).\n"
            "• <b>✏️ Edit:</b> Update contact details, GPS location, or specialty list.\n"
            "• <b>🖼 My Portfolio:</b> Upload up to 5 quality photos of your completed projects to showcase to clients.\n\n"
            "3️⃣ <b>🟢/🔴 AVAILABILITY STATUS:</b>\n"
            "• <b>🟢 Active Mode:</b> You are ready to accept jobs and visible in search.\n"
            "• <b>🔴 Busy Mode:</b> Enable when taking a break or working on an active task (new alerts paused).\n\n"
            "4️⃣ <b>⭐️ RATINGS & REVIEWS:</b>\n"
            "• Track customer feedback and ratings (1-5 stars) upon project completion.\n\n"
            "5️⃣ <b>⚙️ SETTINGS:</b>\n"
            "• Change interface language and notification preferences.\n\n"
            "6️⃣ <b>📞 SUPPORT:</b>\n"
            "• Contact support team or admin, submit suggestions and inquiries.\n\n"
            "💡 <i>Tip: Fill out your profile completely and upload work samples to portfolio to receive more high-paying jobs!</i>"
        ),
        'btn_leave_feedback': "💬 Leave Feedback / Report",
        'prompt_feedback': "✍️ Please enter your feedback or report:",
        'feedback_received': "✅ Thank you! Your feedback has been sent to the administrator.",

        # Umumiy tugmalar va Xatolik / Fallback
        'btn_back_main': "⬅️ Return to Main Menu",
        'btn_goto_main_menu': "🏠 Go to Main Page",
        'btn_restart_bot': "🔄 Restart Bot (/start)",
        'btn_back': "⬅️ Back",
        'bot_error_msg': "⚠️ <b>Sorry, a system error occurred!</b>\n\nTo restart the bot completely, please tap the command below:\n\n👉 <b>/start</b>",
        'bot_outdated_button_msg': "🔄 <b>System was updated / session expired</b>\n\nTo continue and refresh the bot, tap:\n\n👉 <b>/start</b>",
        'bot_restarted_notification': "🚀 <b>{project_name} bot has been updated!</b>\n\n⚙️ System updates have been applied and all services are running stably.\n\nTo continue using the bot, tap:\n👉 <b>/start</b>",
        'job_status_active_alert': "✅ This job post is currently ACTIVE and open for applications!",
        'job_status_taken_alert': "⚠️ Sorry, this job has already been taken by another specialist!",
        'job_status_closed_alert': "❌ This job posting has been cancelled or closed by the employer!",
        'job_already_applied_alert': "ℹ️ You have already submitted a proposal for this job. Please wait for the employer's response!",
        'prompt_apply_message': "✍️ <b>Send a proposal / message to employer:</b>\n\nJob: <b>#{job_id} — {title}</b>\n\nWrite a short message about your experience, price, or estimated arrival time:\n<i>(e.g., Hello, I have 5 years experience and can arrive in 30 minutes)</i>",
        'apply_confirm_title': "📋 <b>CONFIRM PROPOSAL:</b>\n\n📢 <b>Job:</b> #{job_id} — {title}\n✉️ <b>Your Message:</b>\n<i>\"{msg}\"</i>\n\nSend proposal to employer?",
        'btn_send_proposal': "🚀 Send Proposal",
        'btn_edit_proposal': "✏️ Edit",
        'btn_cancel_proposal': "❌ Cancel",
        'apply_success_msg': "🎉 <b>Your proposal has been successfully sent to the employer!</b>\n\nThe employer will review your profile and message to contact you. Please await their reply.",
        'portfolio_full': "⚠️ Maximum 5 portfolio photos allowed!",
        'photo_uploaded_success': "✅ Photo successfully added to portfolio!",
        'photo_deleted_success': "🗑 Photo deleted from portfolio.",
        'caption_updated_success': "✅ Caption updated successfully!",
        'photo_replaced_success': "✅ Photo replaced successfully!",
    }
}

def t(key: str, lang: str = 'uz', **kwargs) -> str:
    lang_dict = TEXTS.get(lang, TEXTS['uz'])
    text = lang_dict.get(key, TEXTS['uz'].get(key, key))
    
    if 'project_name' not in kwargs:
        try:
            from bot_control.models import BotConfig
            kwargs['project_name'] = BotConfig.get_project_name()
        except Exception:
            kwargs['project_name'] = "IshBazari"
            
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            for k, v in kwargs.items():
                text = text.replace(f"{{{k}}}", str(v))
            return text
    return text
