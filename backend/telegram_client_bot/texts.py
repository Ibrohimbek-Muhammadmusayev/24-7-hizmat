TEXTS = {
    'uz': {
        # 0. Auth & Kirish
        'choose_lang': 'Assalomu alaykum! Iltimos, muloqot tilini tanlang:',
        'lang_selected': '🇺🇿 O\'zbek tili (Lotin) tanlandi.',
        'welcome_employer': 'Assalomu alaykum, <b>{name}</b>! 👋\n\n<b>ISH JOYLASH BOTI</b> (Job Post Enterprise)ga xush kelibsiz!\nBu yerda siz o\'zingizga kerakli mutaxassis yoki ishchilarni tezda topishingiz mumkin.',
        
        'step0_name_title': '👤 <b>0.2 Ism va Familiyangizni kiriting:</b>\n<i>(Masalan: Sardor Rahimov)</i>',
        'step0_phone_title': '📱 <b>Telefon raqamingizni yuboring yoki quyidagi formatda kiriting (+998901234567):</b>',
        'btn_send_phone': '📱 Raqamni yuborish',
        'phone_invalid': '⚠️ Telefon raqami noto\'g\'ri. Iltimos, tugmani bosing yoki +998XXXXXXXXX formatida kiriting:',

        # 0.3 Asosiy Menyu
        'main_menu': '🏢 <b>ISH BERUVCHI BOSHQARUV MARKAZI</b>\n\n👤 <b>Ish beruvchi:</b> {name}\n📞 <b>Tel:</b> {phone}\n📊 <b>Faol e\'lonlar:</b> {active_posts_count} ta\n\nKerakli bo\'limni tanlang:',
        'btn_menu_new_post': '➕ Yangi e\'lon',
        'btn_menu_my_posts': '📑 E\'lonlarim',
        'btn_menu_applications': '👥 Javoblar (Отклики)',
        'btn_menu_profile': '👤 Profilim',
        'btn_menu_switch_bot': '💼 Ish izlayapsizmi?',
        'btn_menu_help': '📞 Qo\'llab-quvvatlash',
        'btn_menu_settings': '⚙️ Sozlamalar',
        'settings_title': '⚙️ <b>SOZLAMALAR BO‘LIMI:</b>\n\nKerakli parametrni tanlang:',
        'btn_settings_lang': '🌐 Tilni o‘zgartirish',
        'choose_new_lang': '🌐 <b>Muloqot tilini tanlang:</b>\n\nIltimos, o‘zingizga qulay tilni tanlang:',
        'lang_updated_success': '✅ <b>Muloqot tili muvaffaqiyatli o‘zgartirildi!</b>',

        # 1-Qadam: Ish formati va Sohasi
        'step1_emp_type_title': '1-QADAM: ISH FORMATINI BELGILASH\n\n1.1 Qanday bandlik turida ishchi kerak?',
        'emp_type_daily': '⚡️ Kunbay',
        'emp_type_permanent': '💼 Doimiy ish',
        
        'step1_cat_title': '1.2 Asosiy xizmat sohasini tanlang:\n(Sahifa {current}/{total})',
        'step1_pos_title': '1.3 Aniq mutaxassislikni (lavozimni) tanlang:\n(Sahifa {current}/{total})',
        
        # 2-Qadam: Tafsilotlar
        'step2_desc_title': '2-QADAM: ISH TAFSILOTLARI VA TALABLAR\n\n2.1 Ish tavsifini yozing:\n<i>(Ish hajmi, bajarilishi kerak bo\'lgan vazifalar, sharoitlar)</i>',
        'step2_photo_title': '📸 Obyekt yoki ish joyi rasmini yuboring (Ixtiyoriy):\nAgar rasm bo\'lmasa, <b>[O\'tkazib yuborish]</b> tugmasini bosing.',
        'btn_skip': '⏩ O\'tkazib yuborish',
        
        'step2_workers_count_title': '2.2 Necha nafar ishchi kerak?',
        'workers_1': '1 nafar',
        'workers_2': '2 nafar',
        'workers_3_5': '3-5 nafar',
        'workers_5_plus': 'Brigada (5+)',
        
        'step2_gender_title': '2.3 Ishchi jinsi bo\'yicha talabingiz:',
        'gender_any': '🤝 Farqi yo\'q',
        'gender_male': '👨 Erkak',
        'gender_female': '👩 Ayol',
        
        'step2_start_time_title': '2.4 Ish qachon boshlanishi kerak?',
        'start_urgent': '⚡️ Tezkor (Bugun)',
        'start_tomorrow': '📅 Ertaga',
        'start_custom': '🗓 Boshqa sana',
        
        'step2_price_title': '2.5 To\'lov miqdori va shartini belgilang:',
        'price_negotiable': '🤝 Kelishiladi',
        'price_fixed_btn': '💵 Aniq summa',
        'step2_enter_price_prompt': '💵 To\'lov summasini kiriting:\n<i>(Masalan: 250 000 so\'m/kun yoki 4 000 000 so\'m/oy)</i>',

        # 3-Qadam: Manzil
        'step3_geo_title': '3-QADAM: ISH MANZILI (Hudud va Lokatsiya)\n\n3.1 Ish joyi lokatsiyasini yuboring (Tizim viloyat va tumanni avto-aniqlaydi):',
        'btn_send_gps': '📍 GPS Lokatsiya',
        'btn_select_region_manually': '🗺 Ro\'yxatdan tanlash',
        'step3_address_title': '3.2 Aniq manzil, mahalla yoki mo\'ljalni kiriting:\n<i>(Masalan: Dehqonobod MFY, 12-maktab yonida)</i>',

        # 4-Qadam: Review & Post
        'step4_review_title': '📄 <b>4-QADAM: E\'LONNI TEKSHIRISH VA TASDIQLASH</b>\n\n📢 <b>E\'LON:</b> {title} ({emp_type})\n👥 <b>Kerakli ishchilar:</b> {workers_count}\n🚻 <b>Jinsi:</b> {gender}\n📝 <b>Tavsif:</b> {desc}\n💰 <b>Haq:</b> {price}\n📍 <b>Manzil:</b> {region}, {district}\n🏠 <b>Mo\'ljal:</b> {address}\n⏱ <b>Boshlanish:</b> {start_time}\n📞 <b>Aloqa:</b> {contact_name} ({contact_phone})\n\nE\'lonni tasdiqlaysizmi?',
        'btn_post_confirm': '✅ E\'lonni joylash',
        'btn_change_contact': '✏️ Raqamni o\'zgartirish',
        'btn_edit_details': '✏️ Tahrirlash',
        'btn_cancel_post': '❌ Bekor qilish',
        
        'post_success': '🎉 <b>E\'loningiz muvaffaqiyatli joylandi!</b>\n\n📡 Tizim ushbu hududdagi barcha mos mutaxassislarga avtomatik push-xabar yubordi.\nNomzodlardan javoblar tushganda sizga darhol bildirishnoma keladi.',
        
        # Mening e'lonlarim
        'my_posts_title': '📑 <b>MENING E\'LONLARIM ({count} ta):</b>\n\nBoshqarish uchun quyidagi e\'lonlardan birini tanlang:',
        'my_posts_empty': 'Sizda hali faol e\'lonlar mavjud emas.',
        'post_detail_card': '📄 <b>E\'lon #{id}: {title}</b>\n\n📊 <b>Holat:</b> {status}\n👥 <b>Kerakli ishchilar:</b> {workers_count} ({gender})\n💰 <b>To\'lov:</b> {price}\n📍 <b>Manzil:</b> {region}, {district}\n⏱ <b>Vaqt:</b> {start_time}\n👀 <b>Ko\'rishlar:</b> {views_count} ta\n📬 <b>Javoblar (Отклик):</b> {applications_count} ta',
        'btn_post_pause': '⏸ To\'xtatish',
        'btn_post_resume': '🟢 Faollashtirish',
        'btn_post_close': '✅ Yopish',
        'btn_post_delete': '🗑 O\'chirish',
        
        # Qo'llab-quvvatlash bo'limi
        'support_title': '📞 <b>QO‘LLAB-QUVVATLASH VA YORDAM:</b>\n\nIsh beruvchilar uchun xizmat va e\'lonlar bo\'yicha yordam markazi:\n\n📞 <b>Call-markaz:</b> {phone}\n⏰ <b>Ish vaqti:</b> 09:00 dan 18:00 gacha\n\nQuyidagi tugmalar orqali administrator bilan bog‘lanishingiz yoki yo‘riqnomani ko‘rishingiz mumkin:',
        'btn_write_admin': '👨‍💻 Administratorga yozish',
        'btn_guide': '📖 Foydalanish qo‘llanmasi',
        'guide_text': (
            '📖 <b>ISH BERUVCHI BOTIDAN FOYDALANISH QO‘LLANMASI</b>\n\n'
            'Ushbu bot orqali siz o‘zingizga kerakli sohalar bo‘yicha e\'lonlar joylab, malakali ishchilar va mutaxassislarni tezkor topishingiz mumkin.\n\n'
            '━━━━━━━━━━━━━━━━━━━━\n'
            '🔘 <b>ASOSIY BO‘LIMLAR VA VAZIFALARI:</b>\n\n'
            '1️⃣ <b>➕ Yangi e\'lon:</b>\n'
            '• Kunbay yoki doimiy ish formatini tanlab, mutaxassislik, ish tavsifi, to\'lov miqdori va manzilni ko\'rsatgan holda e\'lon bering.\n'
            '• E\'lon tasdiqlangach, shu sohadagi barcha nomzodlarga zudlik bilan push-bildirishnoma jo\'natiladi.\n\n'
            '2️⃣ <b>👥 Javoblar (Отклики):</b>\n'
            '• Sizning e\'loningizga qiziqish bildirgan ish izlovchilar ro\'yxati.\n'
            '• Nomzodlarning portfoliosi, reytingi va yozgan taklifini ko\'rib chiqib, mos kelganini bir zumda ishga qabul qilishingiz mumkin.\n\n'
            '3️⃣ <b>📑 E\'lonlarim:</b>\n'
            '• Barcha berilgan e\'lonlarni boshqarish: to\'xtatib turish, qayta yoqish, yopish yoki o\'chirish.\n\n'
            '4️⃣ <b>👤 Profilim:</b>\n'
            '• Shaxsiy ma\'lumotlaringiz va aloqa raqamingizni yangilash.\n\n'
            '💡 <i>Eslatma: Ishchilar tezroq topilishi uchun e\'lon tavsifida ish sharoitlari va to\'lovni aniq ko\'rsatish tavsiya etiladi.</i>'
        ),
        'btn_leave_feedback': '💬 Taklif / Shikoyat qoldirish',
        'prompt_feedback': '✍️ Iltimos, o‘z fikr-mulohazangiz, taklif yoki shikoyatingizni yozib yuboring:',
        'feedback_received': '✅ Rahmat! Xabaringiz ma\'muriyatga muvaffaqiyatli yetkazildi.',

        # Standart tugmalar
        'btn_back': '⬅️ Orqaga',
        'btn_goto_main_menu': '🏠 Bosh sahifa',
        'btn_restart_bot': '🔄 Qayta ishga tushirish',
        'bot_error_msg': '⚠️ <b>Kechirasiz, tizimda kutilmagan nosozlik yuz berdi!</b>\n\nBotni qayta yuklash va ishlashni davom ettirish uchun bosing:\n👉 <b>/start</b>',
        'bot_outdated_button_msg': '🔄 <b>Tizim yangilandi yoki sessiya muddati tugadi</b>\n\nIltimos, botni qayta ishga tushirish uchun bosing:\n👉 <b>/start</b>',
        'bot_restarted_notification': '🚀 <b>{project_name} Ish Beruvchi boti yangilandi!</b>\n\n⚙️ Tizimda yangilanishlar amalga oshirildi va barcha xizmatlar barqaror ishlamoqda.\n\nBotdan foydalanishni davom ettirish uchun bosing:\n👉 <b>/start</b>',
        'help_contact_msg': '📞 <b>Qo\'llab-quvvatlash va Aloqa markazi</b>\n\nSavol va takliflar bo\'yicha operatorlarimizga murojaat qilishingiz mumkin:\n\n☎️ Telefon: +998 (71) 200-00-00\n🤖 Onlayn yordamchi: @fullxizmat_support\n⏰ Ish vaqti: 24/7 uzluksiz',
    },
    'oz': {
        # 0. Auth & Kirish
        'choose_lang': 'Ассалому алайкум! Илтимос, мулоқот тилини танланг:',
        'lang_selected': '🇺🇿 Ўзбек тили (Кирилл) танланди.',
        'welcome_employer': 'Ассалому алайкум, <b>{name}</b>! 👋\n\n<b>ИШ ЖОЙЛАШ БОТИ</b> (Job Post Enterprise)га хуш келибсиз!\nБу ерда сиз ўзингизга керакли мутахассис ёки ишчиларни тезда топишингиз мумкин.',
        
        'step0_name_title': '👤 <b>0.2 Исм ва Фамилиянгизни киритинг:</b>\n<i>(Масалан: Сардор Раҳимов)</i>',
        'step0_phone_title': '📱 <b>Телефон рақамингизни юборинг ёки киритинг (+998901234567):</b>',
        'btn_send_phone': '📱 Рақамни юбориш',
        'phone_invalid': '⚠️ Телефон рақами нотўғри! Илтимос, тугмани босинг ёки +998XXXXXXXXX форматида киритинг:',

        # 0.3 Asosiy Menyu
        'main_menu': '🏢 <b>ИШ БЕРУВЧИ БОШҚАРУВ МАРКАЗИ</b>\n\n👤 <b>Иш берувчи:</b> {name}\n📞 <b>Тел:</b> {phone}\n📊 <b>Фаол э\'лонлар:</b> {active_posts_count} та\n\nКеракли бўлимни танланг:',
        'btn_menu_new_post': '➕ Янги э\'лон',
        'btn_menu_my_posts': '📑 Э\'лонларим',
        'btn_menu_applications': '👥 Жавоблар (Отклики)',
        'btn_menu_profile': '👤 Профилим',
        'btn_menu_switch_bot': '💼 Иш излаяпсизми?',
        'btn_menu_help': '📞 Қўллаб-қувватлаш',
        'btn_menu_settings': '⚙️ Созламалар',
        'settings_title': '⚙️ <b>СОЗЛАМАЛАР БЎЛИМИ:</b>\n\nКеракли параметрни танланг:',
        'btn_settings_lang': '🌐 Тилни ўзгартириш',
        'choose_new_lang': '🌐 <b>Мулоқот тилини танланг:</b>\n\nИлтимос, ўзингизга қулай тилни танланг:',
        'lang_updated_success': '✅ <b>Мулоқот тили муваффақиятли ўзгартирилди!</b>',

        # 1-Qadam: Ish formati va Sohasi
        'step1_emp_type_title': '1-ҚАДАМ: ИШ ФОРМАТИНИ БЕЛГИЛАШ\n\n1.1 Қандай бандлик турида ишчи керак?',
        'emp_type_daily': '⚡️ Кунбай',
        'emp_type_permanent': '💼 Доимий иш',
        
        'step1_cat_title': '1.2 Асосий хизмат соҳасини танланг:\n(Саҳифа {current}/{total})',
        'step1_pos_title': '1.3 Аниқ мутахассисликни (лавозимни) танланг:\n(Саҳифа {current}/{total})',
        
        # 2-Qadam: Tafsilotlar
        'step2_desc_title': '2-ҚАДАМ: ИШ ТАФСИЛОТЛАРИ ВА ТАЛАБЛАР\n\n2.1 Иш тавсифини ёзинг:\n<i>(Иш ҳажми, бажарилиши керак бўлган вазифалар, шароитлар)</i>',
        'step2_photo_title': '📸 Объект ёки иш жойи расмини юборинг (Ихтиёрий):\nАгар расм бўлмаса, <b>[Ўтказиб юбориш]</b> тугмасини босинг.',
        'btn_skip': '⏩ Ўтказиб юбориш',
        
        'step2_workers_count_title': '2.2 Неча нафар ишчи керак?',
        'workers_1': '1 нафар',
        'workers_2': '2 нафар',
        'workers_3_5': '3-5 нафар',
        'workers_5_plus': 'Бригада (5+)',
        
        'step2_gender_title': '2.3 Ишчи жинси бўйича талабингиз:',
        'gender_any': '🤝 Фарқи йўқ',
        'gender_male': '👨 Эркак',
        'gender_female': '👩 Аёл',
        
        'step2_start_time_title': '2.4 Иш қачон бошланиши керак?',
        'start_urgent': '⚡️ Тезкор (Бугун)',
        'start_tomorrow': '📅 Эртага',
        'start_custom': '🗓 Бошқа сана',
        
        'step2_price_title': '2.5 Тўлов миқдори ва шартини белгиланг:',
        'price_negotiable': '🤝 Келишилади',
        'price_fixed_btn': '💵 Аниқ сумма',
        'step2_enter_price_prompt': '💵 Тўлов суммасини киритинг:\n<i>(Масалан: 250 000 сўм/кун ёки 4 000 000 сўм/ой)</i>',

        # 3-Qadam: Manzil
        'step3_geo_title': '3-ҚАДАМ: ИШ МАНЗИЛИ (Ҳудуд ва Локация)\n\n3.1 Иш жойи локациясини юборинг (Тизим вилоят ва туманни авто-аниқлайди):',
        'btn_send_gps': '📍 GPS Локация',
        'btn_select_region_manually': '🗺 Рўйхатдан танлаш',
        'step3_address_title': '3.2 Аниқ манзил, маҳалла ёки мўлжални киритинг:\n<i>(Масалан: Деҳқонобод МФЙ, 12-мактаб ёнида)</i>',

        # 4-Qadam: Review & Post
        'step4_review_title': '📄 <b>4-ҚАДАМ: Э\'ЛОННИ ТЕКШИРИШ ВА ТАСДИҚЛАШ</b>\n\n📢 <b>Э\'ЛОН:</b> {title} ({emp_type})\n👥 <b>Керакли ишчилар:</b> {workers_count}\n🚻 <b>Жинси:</b> {gender}\n📝 <b>Тавсиф:</b> {desc}\n💰 <b>Ҳақ:</b> {price}\n📍 <b>Манзил:</b> {region}, {district}\n🏠 <b>Мўлжал:</b> {address}\n⏱ <b>Бошланиш:</b> {start_time}\n📞 <b>Алоқа:</b> {contact_name} ({contact_phone})\n\nЭ\'лонни тасдиқлайсизми?',
        'btn_post_confirm': '✅ Э\'лонни жойлаш',
        'btn_change_contact': '✏️ Рақамни ўзгартириш',
        'btn_edit_details': '✏️ Таҳрирлаш',
        'btn_cancel_post': '❌ Бекор қилиш',
        
        'post_success': '🎉 <b>Э\'лонингиз муваффақиятли жойланди!</b>\n\n📡 Тизим ушбу ҳудуддаги барча мос мутахассисларга автоматик пуш-хабар юборди.\nНомзодлардан жавоблар тушганда сизга дарҳол билдиришнома келади.',
        
        # Mening e'lonlarim
        'my_posts_title': '📑 <b>МЕНИНГ Э\'ЛОНЛАРИМ ({count} та):</b>\n\nБошқариш учун қуйидаги э\'лонлардан бирини танланг:',
        'my_posts_empty': 'Сизда ҳали фаол э\'лонлар мавжуд эмас.',
        'post_detail_card': '📄 <b>Э\'лон #{id}: {title}</b>\n\n📊 <b>Ҳолат:</b> {status}\n👥 <b>Керакли ишчилар:</b> {workers_count} ({gender})\n💰 <b>Тўлов:</b> {price}\n📍 <b>Манзил:</b> {region}, {district}\n⏱ <b>Вақт:</b> {start_time}\n👀 <b>Кўришлар:</b> {views_count} та\n📬 <b>Жавоблар (Отклик):</b> {applications_count} та',
        'btn_post_pause': '⏸ Тўхтатиш',
        'btn_post_resume': '🟢 Фаоллаштириш',
        'btn_post_close': '✅ Ёпиш',
        'btn_post_delete': '🗑 Ўчириш',
        
        # Qo'llab-quvvatlash
        'support_title': '📞 <b>ҚЎЛЛАБ-ҚУВВАТЛАШ ВА ЁРДАМ:</b>\n\nИш берувчилар учун хизмат ва э\'лонлар бўйича ёрдам маркази:\n\n📞 <b>Call-марказ:</b> {phone}\n⏰ <b>Иш вақти:</b> 09:00 дан 18:00 гача',
        'btn_write_admin': '👨‍💻 Администраторга ёзиш',
        'btn_guide': '📖 Фойдаланиш қўлланмаси',
        'guide_text': '📖 <b>ИШ БЕРУВЧИ БОТИДАН ФОЙДАЛАНИШ ҚЎЛЛАНМАСИ</b>\n\nУшбу бот орқали сиз керакли мутахассисларни тезкор топишингиз ва вакансияларингизни бошқаришингиз мумкин.',
        'btn_leave_feedback': '💬 Таклиф / Шикоят қолдириш',
        'prompt_feedback': '✍️ Илтимос, фикр-мулоҳазангиз ёки таклифингизни ёзинг:',
        'feedback_received': '✅ Раҳмат! Хабарингиз маъмуриятга етказилди.',

        # Standart tugmalar
        'btn_back': '⬅️ Орқага',
        'btn_goto_main_menu': '🏠 Бош саҳифа',
        'btn_restart_bot': '🔄 Қайта ишга тушириш',
        'bot_error_msg': '⚠️ <b>Кечирасиз, тизимда кутилмаган носозлик юз берди!</b>\n\nБотни қайта юклаш ва ишлашни давом эттириш учун босинг:\n👉 <b>/start</b>',
        'bot_outdated_button_msg': '🔄 <b>Тизим янгиланди ёки сессия муддати тугади</b>\n\nИлтимос, ботни қайта ишга тушириш учун босинг:\n👉 <b>/start</b>',
        'bot_restarted_notification': '🚀 <b>{project_name} Иш Берувчи боти янгиланди!</b>\n\n⚙️ Тизимда янгиланишлар амалга оширилди ва барча хизматлар барқарор ишламоқда.\n\nБотдан фойдаланишни давом эттириш учун босинг:\n👉 <b>/start</b>',
        'help_contact_msg': '📞 <b>Қўллаб-қувватлаш маркази</b>\n\n☎️ Тел: +998 (71) 200-00-00\n🤖 Онлайн ёрдамчи: @fullxizmat_support\n⏰ Иш вақти: 24/7 узлуксиз',
    },
    'ru': {
        # 0. Auth & Kirish
        'choose_lang': 'Здравствуйте! Пожалуйста, выберите язык:',
        'lang_selected': '🇷🇺 Выбран русский язык.',
        'welcome_employer': 'Здравствуйте, <b>{name}</b>! 👋\n\nДобро пожаловать в <b>Бот размещения вакансий</b> (Job Post Enterprise)!\nЗдесь вы можете быстро найти проверенных специалистов и работников.',
        
        'step0_name_title': '👤 <b>0.2 Введите ваше Имя и Фамилию:</b>\n<i>(Например: Сардор Рахимов)</i>',
        'step0_phone_title': '📱 <b>Отправьте или введите номер телефона (+998901234567):</b>',
        'btn_send_phone': '📱 Отправить номер',
        'phone_invalid': '⚠️ Неверный номер телефона! Нажмите кнопку или введите в формате +998XXXXXXXXX:',

        # 0.3 Asosiy Menyu
        'main_menu': '🏢 <b>ЦЕНТР УПРАВЛЕНИЯ РАБОТОДАТЕЛЯ</b>\n\n👤 <b>Работодатель:</b> {name}\n📞 <b>Тел:</b> {phone}\n📊 <b>Активные вакансии:</b> {active_posts_count} шт.\n\nВыберите нужный раздел:',
        'btn_menu_new_post': '➕ Разместить',
        'btn_menu_my_posts': '📑 Мои вакансии',
        'btn_menu_applications': '👥 Отклики',
        'btn_menu_profile': '👤 Профиль',
        'btn_menu_switch_bot': '💼 Ищете работу?',
        'btn_menu_help': '📞 Поддержка',
        'btn_menu_settings': '⚙️ Настройки',
        'settings_title': '⚙️ <b>РАЗДЕЛ НАСТРОЕК:</b>\n\nВыберите нужный параметр:',
        'btn_settings_lang': '🌐 Изменить язык',
        'choose_new_lang': '🌐 <b>Выберите язык интерфейса:</b>\n\nПожалуйста, выберите удобный для вас язык:',
        'lang_updated_success': '✅ <b>Язык интерфейса успешно изменен!</b>',

        # 1-Qadam: Ish formati va Sohasi
        'step1_emp_type_title': 'ШАГ 1: ФОРМАТ РАБОТЫ\n\n1.1 Какой формат занятости требуется?',
        'emp_type_daily': '⚡️ Посуточно',
        'emp_type_permanent': '💼 Постоянно',
        
        'step1_cat_title': '1.2 Выберите категорию услуг:\n(Страница {current}/{total})',
        'step1_pos_title': '1.3 Выберите точную специальность:\n(Страница {current}/{total})',
        
        # 2-Qadam: Tafsilotlar
        'step2_desc_title': 'ШАГ 2: ДЕТАЛИ И ТРЕБОВАНИЯ\n\n2.1 Напишите описание работы:\n<i>(Объем работы, условия, задачи)</i>',
        'step2_photo_title': '📸 Отправьте фото объекта или рабочего места (Необязательно):\nЕсли фото нет, нажмите <b>[Пропустить]</b>.',
        'btn_skip': '⏩ Пропустить',
        
        'step2_workers_count_title': '2.2 Сколько работников требуется?',
        'workers_1': '1 человек',
        'workers_2': '2 человека',
        'workers_3_5': '3-5 человек',
        'workers_5_plus': 'Бригада (5+)',
        
        'step2_gender_title': '2.3 Требование к полу работника:',
        'gender_any': '🤝 Любой',
        'gender_male': '👨 Мужчина',
        'gender_female': '👩 Женщина',
        
        'step2_start_time_title': '2.4 Когда нужно приступить к работе?',
        'start_urgent': '⚡️ Срочно (Сегодня)',
        'start_tomorrow': '📅 Завтра',
        'start_custom': '🗓 Другая дата',
        
        'step2_price_title': '2.5 Укажите оплату и условия:',
        'price_negotiable': '🤝 Договорная',
        'price_fixed_btn': '💵 Точная сумма',
        'step2_enter_price_prompt': '💵 Введите сумму оплаты:\n<i>(Например: 250 000 сум/день или 4 000 000 сум/месяц)</i>',

        # 3-Qadam: Manzil
        'step3_geo_title': 'ШАГ 3: МЕСТО РАБОТЫ (Локация)\n\n3.1 Отправьте GPS-локацию объекта (Система определит регион и район автоматически):',
        'btn_send_gps': '📍 Отправить GPS',
        'btn_select_region_manually': '🗺 Из списка',
        'step3_address_title': '3.2 Введите точный адрес или ориентир:\n<i>(Например: махалля Дехканабад, возле школы №12)</i>',

        # 4-Qadam: Review & Post
        'step4_review_title': '📄 <b>ШАГ 4: ПРОВЕРКА И ПОДТВЕРЖДЕНИЕ ОБЪЯВЛЕНИЯ</b>\n\n📢 <b>ВАКАНСИЯ:</b> {title} ({emp_type})\n👥 <b>Требуется работников:</b> {workers_count}\n🚻 <b>Пол:</b> {gender}\n📝 <b>Описание:</b> {desc}\n💰 <b>Оплата:</b> {price}\n📍 <b>Адрес:</b> {region}, {district}\n🏠 <b>Ориентир:</b> {address}\n⏱ <b>Начало:</b> {start_time}\n📞 <b>Контакты:</b> {contact_name} ({contact_phone})\n\nПодтверждаете публикацию?',
        'btn_post_confirm': '✅ Опубликовать',
        'btn_change_contact': '✏️ Изменить номер',
        'btn_edit_details': '✏️ Изменить',
        'btn_cancel_post': '❌ Отмена',
        
        'post_success': '🎉 <b>Ваше объявление успешно опубликовано!</b>\n\n📡 Система автоматически разослала push-уведомления подходящим соискателям в вашем районе.\nКак только поступят отклики, вы получите уведомление.',
        
        # Mening e'lonlarim
        'my_posts_title': '📑 <b>МОИ ОБЪЯВЛЕНИЯ ({count} шт.):</b>\n\nВыберите объявление для управления:',
        'my_posts_empty': 'У вас пока нет активных объявлений.',
        'post_detail_card': '📄 <b>Объявление #{id}: {title}</b>\n\n📊 <b>Статус:</b> {status}\n👥 <b>Требуется работников:</b> {workers_count} ({gender})\n💰 <b>Оплата:</b> {price}\n📍 <b>Адрес:</b> {region}, {district}\n⏱ <b>Время:</b> {start_time}\n👀 <b>Просмотры:</b> {views_count}\n📬 <b>Отклики:</b> {applications_count}',
        'btn_post_pause': '⏸ Приостановить',
        'btn_post_resume': '🟢 Активировать',
        'btn_post_close': '✅ Закрыть',
        'btn_post_delete': '🗑 Удалить',
        
        # Qo'llab-quvvatlash
        'support_title': '📞 <b>СЛУЖБА ПОДДЕРЖКИ:</b>\n\nЦентр помощи для работодателей:\n\n📞 <b>Колл-центр:</b> {phone}\n⏰ <b>Время работы:</b> 09:00 - 18:00',
        'btn_write_admin': '👨‍💻 Связаться с админом',
        'btn_guide': '📖 Инструкция',
        'guide_text': '📖 <b>РУКОВОДСТВО ДЛЯ РАБОТОДАТЕЛЕЙ</b>\n\nЗдесь вы можете легко размещать вакансии и быстро находить исполнителей.',
        'btn_leave_feedback': '💬 Оставить отзыв / жалобу',
        'prompt_feedback': '✍️ Пожалуйста, напишите ваше сообщение:',
        'feedback_received': '✅ Спасибо! Сообщение отправлено администрации.',

        # Standart tugmalar
        'btn_back': '⬅️ Назад',
        'btn_goto_main_menu': '🏠 Главное меню',
        'btn_restart_bot': '🔄 Перезапустить',
        'bot_error_msg': '⚠️ <b>Произошла непредвиденная системная ошибка!</b>\n\nЧтобы перезапустить бота и продолжить работу, нажмите:\n👉 <b>/start</b>',
        'bot_outdated_button_msg': '🔄 <b>Система обновлена или сессия устарела</b>\n\nПожалуйста, нажмите для перезапуска бота:\n👉 <b>/start</b>',
        'bot_restarted_notification': '🚀 <b>Бот работодателя {project_name} обновлен!</b>\n\n⚙️ Были установлены системные обновления, и все сервисы работают стабильно.\n\nЧтобы продолжить работу с ботом, нажмите:\n👉 <b>/start</b>',
        'help_contact_msg': '📞 <b>Служба поддержки {project_name}</b>\n\n☎️ Телефон: +998 (71) 200-00-00\n🤖 Онлайн-помощник: @fullxizmat_support\n⏰ Режим работы: 24/7 круглосуточно',
    },
    'en': {
        # 0. Auth & Kirish
        'choose_lang': 'Hello! Please select your language:',
        'lang_selected': '🇬🇧 English language selected.',
        'welcome_employer': 'Welcome, <b>{name}</b>! 👋\n\nWelcome to <b>Job Post Enterprise Bot</b>!\nHere you can easily post jobs and hire qualified specialists and workers.',
        
        'step0_name_title': '👤 <b>0.2 Enter your Full Name:</b>\n<i>(e.g., Sardor Rahimov)</i>',
        'step0_phone_title': '📱 <b>Share or enter your phone number (+998901234567):</b>',
        'btn_send_phone': '📱 Send Phone',
        'phone_invalid': '⚠️ Invalid phone number format! Tap button or enter in +998XXXXXXXXX format:',

        # 0.3 Asosiy Menyu
        'main_menu': '🏢 <b>EMPLOYER DASHBOARD</b>\n\n👤 <b>Employer:</b> {name}\n📞 <b>Phone:</b> {phone}\n📊 <b>Active Job Posts:</b> {active_posts_count}\n\nSelect an option:',
        'btn_menu_new_post': '➕ Post Job',
        'btn_menu_my_posts': '📑 My Posts',
        'btn_menu_applications': '👥 Applications',
        'btn_menu_profile': '👤 Profile',
        'btn_menu_switch_bot': '💼 Looking for a Job?',
        'btn_menu_help': '📞 Support',
        'btn_menu_settings': '⚙️ Settings',
        'settings_title': '⚙️ <b>SETTINGS:</b>\n\nSelect a setting to configure:',
        'btn_settings_lang': '🌐 Change Language',
        'choose_new_lang': '🌐 <b>Choose your preferred language:</b>\n\nPlease select a language:',
        'lang_updated_success': '✅ <b>Language successfully updated!</b>',

        # 1-Qadam: Ish formati va Sohasi
        'step1_emp_type_title': 'STEP 1: JOB FORMAT\n\n1.1 What type of employment do you need?',
        'emp_type_daily': '⚡️ Daily Gig',
        'emp_type_permanent': '💼 Full-time',
        
        'step1_cat_title': '1.2 Select the main category:\n(Page {current}/{total})',
        'step1_pos_title': '1.3 Select the specific job title:\n(Page {current}/{total})',
        
        # 2-Qadam: Tafsilotlar
        'step2_desc_title': 'STEP 2: JOB DETAILS & REQUIREMENTS\n\n2.1 Describe the job requirements:\n<i>(Scope of work, conditions, requirements)</i>',
        'step2_photo_title': '📸 Send a photo of the workspace/object (Optional):\nIf no photo, tap <b>[Skip]</b>.',
        'btn_skip': '⏩ Skip',
        
        'step2_workers_count_title': '2.2 How many workers do you need?',
        'workers_1': '1 worker',
        'workers_2': '2 workers',
        'workers_3_5': '3-5 workers',
        'workers_5_plus': 'Crew (5+)',
        
        'step2_gender_title': '2.3 Gender preference for workers:',
        'gender_any': '🤝 Any',
        'gender_male': '👨 Male',
        'gender_female': '👩 Female',
        
        'step2_start_time_title': '2.4 When should work start?',
        'start_urgent': '⚡️ Urgent (Today)',
        'start_tomorrow': '📅 Tomorrow',
        'start_custom': '🗓 Custom Date',
        
        'step2_price_title': '2.5 Specify payment and compensation:',
        'price_negotiable': '🤝 Negotiable',
        'price_fixed_btn': '💵 Fixed Price',
        'step2_enter_price_prompt': '💵 Enter payment amount:\n<i>(e.g., 250,000 UZS/day or 4,000,000 UZS/month)</i>',

        # 3-Qadam: Manzil
        'step3_geo_title': 'STEP 3: WORK LOCATION\n\n3.1 Send GPS location (The system automatically determines region and district):',
        'btn_send_gps': '📍 Send GPS',
        'btn_select_region_manually': '🗺 Choose List',
        'step3_address_title': '3.2 Enter exact address or landmark:\n<i>(e.g., Dehqonobod mahalla, near school #12)</i>',

        # 4-Qadam: Review & Post
        'step4_review_title': '📄 <b>STEP 4: REVIEW & CONFIRM JOB POST</b>\n\n📢 <b>JOB:</b> {title} ({emp_type})\n👥 <b>Required Workers:</b> {workers_count}\n🚻 <b>Gender:</b> {gender}\n📝 <b>Description:</b> {desc}\n💰 <b>Payment:</b> {price}\n📍 <b>Location:</b> {region}, {district}\n🏠 <b>Address:</b> {address}\n⏱ <b>Start:</b> {start_time}\n📞 <b>Contact:</b> {contact_name} ({contact_phone})\n\nConfirm posting this job?',
        'btn_post_confirm': '✅ Post Job',
        'btn_change_contact': '✏️ Change Phone',
        'btn_edit_details': '✏️ Edit',
        'btn_cancel_post': '❌ Cancel',
        
        'post_success': '🎉 <b>Your job has been successfully posted!</b>\n\n📡 Push notifications were automatically sent to matching specialists in your area.\nYou will receive instant notifications when workers apply.',
        
        # Mening e'lonlarim
        'my_posts_title': '📑 <b>MY JOB POSTS ({count}):</b>\n\nSelect a post to manage:',
        'my_posts_empty': 'You have no active job posts currently.',
        'post_detail_card': '📄 <b>Job #{id}: {title}</b>\n\n📊 <b>Status:</b> {status}\n👥 <b>Required Workers:</b> {workers_count} ({gender})\n💰 <b>Payment:</b> {price}\n📍 <b>Location:</b> {region}, {district}\n⏱ <b>Time:</b> {start_time}\n👀 <b>Views:</b> {views_count}\n📬 <b>Applications:</b> {applications_count}',
        'btn_post_pause': '⏸ Pause',
        'btn_post_resume': '🟢 Resume',
        'btn_post_close': '✅ Close',
        'btn_post_delete': '🗑 Delete',
        
        # Qo'llab-quvvatlash
        'support_title': '📞 <b>CUSTOMER SUPPORT:</b>\n\nHelp center for employers:\n\n📞 <b>Call center:</b> {phone}\n⏰ <b>Working hours:</b> 09:00 - 18:00',
        'btn_write_admin': '👨‍💻 Contact Admin',
        'btn_guide': '📖 User Guide',
        'guide_text': '📖 <b>EMPLOYER BOT USER GUIDE</b>\n\nEasily post job vacancies and quickly hire verified workers and specialists.',
        'btn_leave_feedback': '💬 Leave Feedback / Report',
        'prompt_feedback': '✍️ Please write your feedback or proposal:',
        'feedback_received': '✅ Thank you! Your message has been sent to administrators.',

        # Standart tugmalar
        'btn_back': '⬅️ Back',
        'btn_goto_main_menu': '🏠 Main Menu',
        'btn_restart_bot': '🔄 Restart',
        'bot_error_msg': '⚠️ <b>An unexpected system error occurred!</b>\n\nTo restart the bot and continue, please tap:\n👉 <b>/start</b>',
        'bot_outdated_button_msg': '🔄 <b>System was updated or session expired</b>\n\nPlease tap below to restart the bot:\n👉 <b>/start</b>',
        'bot_restarted_notification': '🚀 <b>{project_name} Employer bot has been updated!</b>\n\n⚙️ System updates have been applied and all services are running stably.\n\nTo continue using the bot, tap:\n👉 <b>/start</b>',
        'help_contact_msg': '📞 <b>{project_name} Customer Support</b>\n\n☎️ Phone: +998 (71) 200-00-00\n🤖 Online Assistant: @fullxizmat_support\n⏰ Working hours: 24/7 non-stop',
    }
}

def t(key, lang='uz', **kwargs):
    l_dict = TEXTS.get(lang, TEXTS['uz'])
    template = l_dict.get(key, TEXTS['uz'].get(key, key))
    
    if 'project_name' not in kwargs:
        try:
            from bot_control.models import BotConfig
            kwargs['project_name'] = BotConfig.get_project_name()
        except Exception:
            kwargs['project_name'] = "IshBazari"

    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            for k, v in kwargs.items():
                template = template.replace(f"{{{k}}}", str(v))
            return template
    return template

