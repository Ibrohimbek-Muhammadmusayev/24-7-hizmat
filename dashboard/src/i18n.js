// Multi-language dictionary supporting 4 languages:
// 'uz' -> O'zbekcha (Lotin)
// 'oz' (or 'kr') -> Ўзбекча (Кирилл)
// 'ru' -> Русский
// 'en' -> English

export const translations = {
  uz: {
    // Header & Modes
    app_title: "IshBazari",
    worker_mode: "Usta kabineti",
    employer_mode: "Ish beruvchi",
    switch_to_employer: "Ish beruvchi",
    switch_to_worker: "Usta",
    status_active: "Faol",
    status_busy: "Band",
    busy_banner: "Siz hozir BAND holatdasiz. Yangi xabarlar kelmay turadi.",
    make_active: "Faol qilish",

    // Search & Filters
    search_placeholder: "Ish nomi, tuman yoki kalit so'z bo'yicha qidiring...",
    filter_all_jobs: "Barcha ishlar",
    filter_daily: "Kunbay",
    filter_permanent: "Doimiy",
    filter_my_district: "O'z tumanim",
    filter_my_region: "Butun viloyat",
    all_categories: "Barcha sohalar",
    available_jobs_count: "Mavjud ishlar",
    refresh: "Yangilash",
    loading_jobs: "Ish e'lonlari yuklanmoqda...",
    no_jobs_found: "Mos ishlar topilmadi",
    no_jobs_desc: "Hozirda tanlangan mezonlar bo'yicha e'lonlar yo'q. Qidiruv mezonlarini o'zgartiring.",
    clear_filters: "Filtrlarni tozalash",

    // Job Cards
    daily_badge: "Kunbay ish",
    permanent_badge: "Doimiy ish",
    urgent_badge: "Shoshilinch",
    planned_badge: "Rejali",
    salary_negotiable: "Kelishilgan narxda",
    salary_fixed: "so'm",
    workers_needed: "Kerak",
    apply_btn: "Ariza topshirish",
    applied_badge: "Ariza yuborilgan",
    time_posted: "joylandi",

    // Job Detail Modal
    job_details: "Ish haqida batafsil",
    job_category: "Soha",
    job_location: "Manzil / Hudud",
    job_start: "Boshlanish vaqti",
    job_salary: "To'lov summasi",
    job_description: "Batafsil talablar",
    send_proposal: "Ishga ariza (otklik) yuborish",
    proposal_placeholder: "Assalomu alaykum, men ushbu ishni sifatli bajarib bera olaman...",
    proposal_label: "Ish beruvchiga xabar (ixtiyoriy):",
    confirm_apply: "Arizani tasdiqlash",
    apply_success: "Arizangiz muvaffaqiyatli yuborildi!",

    // Worker - My Applications
    my_applications_title: "Yuborgan Arizalarim",
    my_applications_desc: "Ish beruvchilarga yuborgan arizalaringiz va ularning holati",
    loading_applications: "Arizalar yuklanmoqda...",
    no_applications: "Hozircha arizalar yo'q",
    no_applications_desc: "Siz hali birorta ham ish e'loniga ariza yubormadingiz.",
    find_jobs_btn: "Ishlarni ko'rish",
    app_status_pending: "Ko'rib chiqilmoqda",
    app_status_accepted: "Qabul qilindi",
    app_status_rejected: "Rad etildi",

    // Employer - Post Job Form
    post_job_title: "Yangi E'lon Joylashtirish",
    post_job_desc: "Talablaringizni kiriting va malakali ustalarni tez toping",
    emp_type_label: "Ish turi",
    category_label: "Soha / Yo'nalish",
    select_category: "Sohani tanlang",
    position_title_label: "Ish / Kasb nomi",
    position_title_placeholder: "Masalan: Gipsokarton ustasi, Santexnik...",
    desc_label: "Batafsil tavsif va talablar",
    desc_placeholder: "Ish hajmi, talablar va sharoitlarni batafsil yozing...",
    workers_count_label: "Kerakli ishchilar soni",
    salary_label: "To'lov narxi (so'mda)",
    salary_placeholder: "Masalan: 250000",
    is_negotiable: "Narx kelishiladi",
    district_label: "Tuman / Shahar",
    district_placeholder: "Masalan: Chilonzor tumani",
    address_label: "Aniq manzil yoki mo'ljal",
    address_placeholder: "Ko'cha, uy yoki mo'ljal",
    contact_name_label: "Aloqa uchun ism",
    contact_phone_label: "Telefon raqam",
    submit_post_btn: "E'lonni chop etish",
    post_success_msg: "E'lon muvaffaqiyatli chop etildi!",

    // Employer - My Posts
    my_posts_title: "Mening E'lonlarim",
    my_posts_desc: "Siz yaratgan ish e'lonlari va ularga tushgan arizalar",
    no_posts_yet: "Hozircha e'lonlar yo'q",
    no_posts_desc: "Siz hali e'lon joylashtirmadingiz. Yangi ishchilar topish uchun e'lon bering.",
    post_now_btn: "E'lon berish",
    applicants_count: "tushgan arizalar",

    // Profile & Cabinet
    cabinet_title: "Shaxsiy Kabinet",
    edit_profile_btn: "Tahrirlash",
    successful_jobs: "ta muvaffaqiyatli ish",
    phone_number: "Telefon raqam",
    not_entered: "Kiritilmagan",
    region_district: "Hudud / Tuman",
    gps_location: "GPS Lokatsiya",
    not_attached: "Biriktirilmagan",
    app_language: "Dastur tili",
    account_status: "Hisob holati",
    status_verified: "Faol / Tasdiqlangan",
    change_language_btn: "Tilni o'zgartirish",
    update_location_btn: "Lokatsiyani yangilash",
    location_updating: "Aniqlanmoqda...",
    location_updated_success: "Lokatsiyangiz muvaffaqiyatli yangilandi!",
    support_btn: "Qo'llab-quvvatlash va Takliflar",

    // Language Modal
    select_language_title: "Dastur tilini tanlang",
    lang_uz: "O'zbekcha (Lotin)",
    lang_oz: "Ўзбекча (Кирилл)",
    lang_ru: "Русский",
    lang_en: "English",

    // Profile Edit Modal
    edit_profile_title: "Profil Ma'lumotlarini Tahrirlash",
    full_name_label: "Ism Familiya",
    cancel_btn: "Bekor qilish",
    save_btn: "Saqlash",

    // Support Form
    support_title: "Qo'llab-quvvatlash va Takliflar",
    support_desc: "Tizim bo'yicha savol, taklif yoki shikoyatingiz bo'lsa, xabar qoldiring.",
    message_sent_success: "Xabaringiz qabul qilindi!",
    admin_review_soon: "Ma'muriyat tez orada ko'rib chiqadi.",
    message_text_label: "Xabaringiz matni:",
    message_placeholder: "Taklif yoki muammoingizni yozib qoldiring...",
    back_btn: "Orqaga",
    send_btn: "Yuborish",

    // Navigation Tabs
    nav_jobs: "Ishlar",
    nav_my_apps: "Arizalarim",
    nav_cabinet: "Kabinet",
    nav_my_posts: "E'lonlarim",
    nav_post_job: "E'lon Berish"
  },

  oz: {
    // Header & Modes
    app_title: "IshBazari",
    worker_mode: "Уста кабинети",
    employer_mode: "Иш берувчи",
    switch_to_employer: "Иш берувчи",
    switch_to_worker: "Уста",
    status_active: "Фаол",
    status_busy: "Банд",
    busy_banner: "Сиз ҳозир БАНД ҳолатдасиз. Янги хабарлар келмай туради.",
    make_active: "Фаол қилиш",

    // Search & Filters
    search_placeholder: "Иш номи, туман ёки калит сўз бўйича қидиринг...",
    filter_all_jobs: "Барча ишлар",
    filter_daily: "Кунбай",
    filter_permanent: "Доимий",
    filter_my_district: "Ўз туманим",
    filter_my_region: "Бутун вилоят",
    all_categories: "Барча соҳалар",
    available_jobs_count: "Мавжуд ишлар",
    refresh: "Янгилаш",
    loading_jobs: "Иш эълонлари юкланмоқда...",
    no_jobs_found: "Мос ишлар топилмади",
    no_jobs_desc: "Ҳозирда танланган мезонлар бўйича эълонлар йўқ. Қидирув мезонларини ўзгартиринг.",
    clear_filters: "Фильтрларни тозалаш",

    // Job Cards
    daily_badge: "Кунбай иш",
    permanent_badge: "Доимий иш",
    urgent_badge: "Шошилинч",
    planned_badge: "Режали",
    salary_negotiable: "Келишилган нархда",
    salary_fixed: "сўм",
    workers_needed: "Керак",
    apply_btn: "Ариза топшириш",
    applied_badge: "Ариза юборилган",
    time_posted: "жойланди",

    // Job Detail Modal
    job_details: "Иш ҳақида батафсил",
    job_category: "Соҳа",
    job_location: "Манзил / Ҳудуд",
    job_start: "Бошланиш вақти",
    job_salary: "Тўлов суммаси",
    job_description: "Батафсил талаблар",
    send_proposal: "Ишга ариза (отклик) юбориш",
    proposal_placeholder: "Ассалому алайкум, мен ушбу ишни сифатли бажариб бера оламан...",
    proposal_label: "Иш берувчига хабар (ихтиёрий):",
    confirm_apply: "Аризани тасдиқлаш",
    apply_success: "Аризангиз муваффақиятли юборилди!",

    // Worker - My Applications
    my_applications_title: "Юборган Аризаларим",
    my_applications_desc: "Иш берувчиларга юборган аризаларингиз ва уларнинг ҳолати",
    loading_applications: "Аризалар юкланмоқда...",
    no_applications: "Ҳозирча аризалар йўқ",
    no_applications_desc: "Сиз ҳали бирорта ҳам иш эълонига ариза юбормадингиз.",
    find_jobs_btn: "Ишларни кўриш",
    app_status_pending: "Кўриб чиқилмоқда",
    app_status_accepted: "Қабул қилинди",
    app_status_rejected: "Рад этилди",

    // Employer - Post Job Form
    post_job_title: "Янги Эълон Жойлаштириш",
    post_job_desc: "Талабларингизни киритинг ва малакали усталарни тез топинг",
    emp_type_label: "Иш тури",
    category_label: "Соҳа / Йўналиш",
    select_category: "Соҳани танланг",
    position_title_label: "Иш / Касб номи",
    position_title_placeholder: "Масалан: Гипсокартон устаси, Сантехник...",
    desc_label: "Батафсил тавсиф ва талаблар",
    desc_placeholder: "Иш ҳажми, талаблар ва шароитларни батафсил ёзинг...",
    workers_count_label: "Керакли ишчилар сони",
    salary_label: "Тўлов нархи (сўмда)",
    salary_placeholder: "Масалан: 250000",
    is_negotiable: "Нарх келишилади",
    district_label: "Туман / Шаҳар",
    district_placeholder: "Масалан: Чилонзор тумани",
    address_label: "Аниқ манзил ёки мўлжал",
    address_placeholder: "Кўча, уй ёки мўлжал",
    contact_name_label: "Алоқа учун исм",
    contact_phone_label: "Телефон рақам",
    submit_post_btn: "Эълонни чоп этиш",
    post_success_msg: "Эълон муваффақиятли чоп этилди!",

    // Employer - My Posts
    my_posts_title: "Менинг Эълонларим",
    my_posts_desc: "Сиз яратган иш эълонлари ва уларга тушган аризалар",
    no_posts_yet: "Ҳозирча эълонлар йўқ",
    no_posts_desc: "Сиз ҳали эълон жойлаштирмадингиз. Янги ишчилар топиш учун эълон беринг.",
    post_now_btn: "Эълон бериш",
    applicants_count: "тушган аризалар",

    // Profile & Cabinet
    cabinet_title: "Шахсий Кабинет",
    edit_profile_btn: "Таҳрирлаш",
    successful_jobs: "та муваффақиятли иш",
    phone_number: "Телефон рақам",
    not_entered: "Киритилмаган",
    region_district: "Ҳудуд / Туман",
    gps_location: "GPS Локация",
    not_attached: "Бириктирилмаган",
    app_language: "Дастур тили",
    account_status: "Ҳисоб ҳолати",
    status_verified: "Фаол / Тасдиқланган",
    change_language_btn: "Тилни ўзгартириш",
    update_location_btn: "Локацияни янгилаш",
    location_updating: "Аниқланмоқда...",
    location_updated_success: "Локациянгиз муваффақиятли янгиланди!",
    support_btn: "Қўллаб-қувватлаш ва Таклифлар",

    // Language Modal
    select_language_title: "Дастур тилини танланг",
    lang_uz: "O'zbekcha (Lotin)",
    lang_oz: "Ўзбекча (Кирилл)",
    lang_ru: "Русский",
    lang_en: "English",

    // Profile Edit Modal
    edit_profile_title: "Профиль Маълумотларини Таҳрирлаш",
    full_name_label: "Исм Фамилия",
    cancel_btn: "Бекор қилиш",
    save_btn: "Сақлаш",

    // Support Form
    support_title: "Қўллаб-қувватлаш ва Таклифлар",
    support_desc: "Тизим бўйича савол, таклиф ёки шикоятингиз бўлса, хабар қолдиринг.",
    message_sent_success: "Хабарингиз қабул қилинди!",
    admin_review_soon: "Маъмурият тез орада кўриб чиқади.",
    message_text_label: "Хабарингиз матни:",
    message_placeholder: "Таклиф ёки муаммоингизни ёзиб қолдиринг...",
    back_btn: "Орқага",
    send_btn: "Юбориш",

    // Navigation Tabs
    nav_jobs: "Ишлар",
    nav_my_apps: "Аризаларим",
    nav_cabinet: "Кабинет",
    nav_my_posts: "Эълонларим",
    nav_post_job: "Эълон Бериш"
  },

  ru: {
    // Header & Modes
    app_title: "IshBazari",
    worker_mode: "Кабинет мастера",
    employer_mode: "Работодатель",
    switch_to_employer: "Работодатель",
    switch_to_worker: "Мастер",
    status_active: "Активен",
    status_busy: "Занят",
    busy_banner: "Вы сейчас в статусе ЗАНЯТ. Новые уведомления временно не приходят.",
    make_active: "Стать активным",

    // Search & Filters
    search_placeholder: "Поиск по названию работы, району или ключевым словам...",
    filter_all_jobs: "Все заказы",
    filter_daily: "Подработка",
    filter_permanent: "Постоянная",
    filter_my_district: "Мой район",
    filter_my_region: "Вся область",
    all_categories: "Все категории",
    available_jobs_count: "Доступно вакансий",
    refresh: "Обновить",
    loading_jobs: "Загрузка вакансий...",
    no_jobs_found: "Подходящих вакансий не найдено",
    no_jobs_desc: "По выбранным критериям заказов пока нет. Попробуйте изменить фильтры.",
    clear_filters: "Сбросить фильтры",

    // Job Cards
    daily_badge: "Подработка / Дневная",
    permanent_badge: "Постоянная работа",
    urgent_badge: "Срочно",
    planned_badge: "Планово",
    salary_negotiable: "По договорённости",
    salary_fixed: "сум",
    workers_needed: "Требуется",
    apply_btn: "Откликнуться",
    applied_badge: "Отклик отправлен",
    time_posted: "назад",

    // Job Detail Modal
    job_details: "Детали заказа",
    job_category: "Сфера",
    job_location: "Адрес / Район",
    job_start: "Время начала",
    job_salary: "Сумма оплаты",
    job_description: "Подробные требования",
    send_proposal: "Отправить отклик на работу",
    proposal_placeholder: "Здравствуйте, я готов качественно выполнить эту работу...",
    proposal_label: "Сообщение работодателю (необязательно):",
    confirm_apply: "Подтвердить отклик",
    apply_success: "Ваш отклик успешно отправлен!",

    // Worker - My Applications
    my_applications_title: "Мои Отклики",
    my_applications_desc: "Список ваших заявок работодателям и их текущий статус",
    loading_applications: "Загрузка заявок...",
    no_applications: "Пока нет откликов",
    no_applications_desc: "Вы ещё не откликались ни на одну вакансию.",
    find_jobs_btn: "Смотреть заказы",
    app_status_pending: "На рассмотрении",
    app_status_accepted: "Принят",
    app_status_rejected: "Отклонён",

    // Employer - Post Job Form
    post_job_title: "Разместить Новую Вакансию",
    post_job_desc: "Укажите ваши требования и быстро найдите проверенных мастеров",
    emp_type_label: "Тип занятости",
    category_label: "Категория / Сфера",
    select_category: "Выберите категорию",
    position_title_label: "Название вакансии / специальности",
    position_title_placeholder: "Например: Гипсокартонщик, Сантехник...",
    desc_label: "Подробное описание и требования",
    desc_placeholder: "Опишите объём работы, требования и условия...",
    workers_count_label: "Количество мастеров",
    salary_label: "Сумма оплаты (в сумах)",
    salary_placeholder: "Например: 250000",
    is_negotiable: "Договорная цена",
    district_label: "Район / Город",
    district_placeholder: "Например: Чиланзарский район",
    address_label: "Точный адрес или ориентир",
    address_placeholder: "Улица, дом или ориентир",
    contact_name_label: "Контактное лицо",
    contact_phone_label: "Номер телефона",
    submit_post_btn: "Опубликовать объявление",
    post_success_msg: "Объявление успешно опубликовано!",

    // Employer - My Posts
    my_posts_title: "Мои Объявления",
    my_posts_desc: "Созданные вами вакансии и отклики мастеров",
    no_posts_yet: "Пока нет объявлений",
    no_posts_desc: "Вы ещё не разместили вакансий. Разместите объявление для поиска мастеров.",
    post_now_btn: "Подать объявление",
    applicants_count: "откликов",

    // Profile & Cabinet
    cabinet_title: "Личный Кабинет",
    edit_profile_btn: "Редактировать",
    successful_jobs: "успешных заказов",
    phone_number: "Номер телефона",
    not_entered: "Не указан",
    region_district: "Регион / Район",
    gps_location: "GPS Локация",
    not_attached: "Не привязана",
    app_language: "Язык приложения",
    account_status: "Статус аккаунта",
    status_verified: "Активен / Подтверждён",
    change_language_btn: "Сменить язык",
    update_location_btn: "Обновить локацию",
    location_updating: "Определение...",
    location_updated_success: "Локация успешно обновлена!",
    support_btn: "Поддержка и предложения",

    // Language Modal
    select_language_title: "Выберите язык приложения",
    lang_uz: "O'zbekcha (Lotin)",
    lang_oz: "Ўзбекча (Кирилл)",
    lang_ru: "Русский",
    lang_en: "English",

    // Profile Edit Modal
    edit_profile_title: "Редактирование Профиля",
    full_name_label: "Имя Фамилия",
    cancel_btn: "Отмена",
    save_btn: "Сохранить",

    // Support Form
    support_title: "Служба Поддержки",
    support_desc: "Если у вас есть вопросы, предложения или жалобы, напишите нам.",
    message_sent_success: "Ваше сообщение принято!",
    admin_review_soon: "Администрация рассмотрит его в ближайшее время.",
    message_text_label: "Текст обращения:",
    message_placeholder: "Опишите ваш вопрос или предложение...",
    back_btn: "Назад",
    send_btn: "Отправить",

    // Navigation Tabs
    nav_jobs: "Вакансии",
    nav_my_apps: "Отклики",
    nav_cabinet: "Кабинет",
    nav_my_posts: "Объявления",
    nav_post_job: "Подать заказ"
  },

  en: {
    // Header & Modes
    app_title: "IshBazari",
    worker_mode: "Worker Dashboard",
    employer_mode: "Employer",
    switch_to_employer: "Employer",
    switch_to_worker: "Worker",
    status_active: "Active",
    status_busy: "Busy",
    busy_banner: "You are currently BUSY. New alerts are paused.",
    make_active: "Set Active",

    // Search & Filters
    search_placeholder: "Search by job title, district or keywords...",
    filter_all_jobs: "All Jobs",
    filter_daily: "Daily Shift",
    filter_permanent: "Full Time",
    filter_my_district: "My District",
    filter_my_region: "Entire Region",
    all_categories: "All Categories",
    available_jobs_count: "Available Jobs",
    refresh: "Refresh",
    loading_jobs: "Loading job offers...",
    no_jobs_found: "No matching jobs found",
    no_jobs_desc: "There are currently no job postings matching your criteria. Try adjusting your filters.",
    clear_filters: "Clear Filters",

    // Job Cards
    daily_badge: "Daily / Shift",
    permanent_badge: "Permanent Job",
    urgent_badge: "Urgent",
    planned_badge: "Scheduled",
    salary_negotiable: "Negotiable rate",
    salary_fixed: "UZS",
    workers_needed: "Needed",
    apply_btn: "Apply Now",
    applied_badge: "Application Sent",
    time_posted: "ago",

    // Job Detail Modal
    job_details: "Job Details",
    job_category: "Category",
    job_location: "Address / Area",
    job_start: "Start Time",
    job_salary: "Payment / Salary",
    job_description: "Full Requirements",
    send_proposal: "Send Application Proposal",
    proposal_placeholder: "Hello, I have the required skills and can complete this job with high quality...",
    proposal_label: "Message to employer (optional):",
    confirm_apply: "Confirm Application",
    apply_success: "Your application has been submitted successfully!",

    // Worker - My Applications
    my_applications_title: "My Applications",
    my_applications_desc: "List of job applications sent to employers and their current status",
    loading_applications: "Loading applications...",
    no_applications: "No applications yet",
    no_applications_desc: "You have not submitted any job proposals yet.",
    find_jobs_btn: "Browse Jobs",
    app_status_pending: "In Review",
    app_status_accepted: "Accepted",
    app_status_rejected: "Declined",

    // Employer - Post Job Form
    post_job_title: "Post a New Job",
    post_job_desc: "Specify your requirements and quickly find skilled workers",
    emp_type_label: "Employment Type",
    category_label: "Category / Trade",
    select_category: "Select a Category",
    position_title_label: "Job / Profession Title",
    position_title_placeholder: "E.g.: Plumber, Electrician, Carpenter...",
    desc_label: "Detailed Description & Requirements",
    desc_placeholder: "Specify the scope of work, conditions and expectations...",
    workers_count_label: "Number of workers needed",
    salary_label: "Payment Amount (UZS)",
    salary_placeholder: "E.g.: 250000",
    is_negotiable: "Price is negotiable",
    district_label: "District / City",
    district_placeholder: "E.g.: Chilanzar district",
    address_label: "Exact Address or Landmark",
    address_placeholder: "Street, building number or landmark",
    contact_name_label: "Contact Person",
    contact_phone_label: "Phone Number",
    submit_post_btn: "Publish Job Offer",
    post_success_msg: "Job offer published successfully!",

    // Employer - My Posts
    my_posts_title: "My Job Offers",
    my_posts_desc: "Job postings you have published and incoming worker applications",
    no_posts_yet: "No job postings yet",
    no_posts_desc: "You haven't posted any jobs yet. Create a job offer to hire workers.",
    post_now_btn: "Post Job",
    applicants_count: "proposals",

    // Profile & Cabinet
    cabinet_title: "Personal Dashboard",
    edit_profile_btn: "Edit Profile",
    successful_jobs: "completed jobs",
    phone_number: "Phone Number",
    not_entered: "Not provided",
    region_district: "Region / District",
    gps_location: "GPS Location",
    not_attached: "Not set",
    app_language: "App Language",
    account_status: "Account Status",
    status_verified: "Active / Verified",
    change_language_btn: "Change Language",
    update_location_btn: "Update Location",
    location_updating: "Locating...",
    location_updated_success: "Location updated successfully!",
    support_btn: "Support & Feedback",

    // Language Modal
    select_language_title: "Select App Language",
    lang_uz: "O'zbekcha (Latin)",
    lang_oz: "Ўзбекча (Cyrillic)",
    lang_ru: "Русский",
    lang_en: "English",

    // Profile Edit Modal
    edit_profile_title: "Edit Profile Details",
    full_name_label: "Full Name",
    cancel_btn: "Cancel",
    save_btn: "Save Changes",

    // Support Form
    support_title: "Help & Feedback",
    support_desc: "Feel free to submit questions, feedback or suggestions directly to administration.",
    message_sent_success: "Your message has been received!",
    admin_review_soon: "Our team will review it shortly.",
    message_text_label: "Your Message:",
    message_placeholder: "Describe your feedback or question...",
    back_btn: "Go Back",
    send_btn: "Submit",

    // Navigation Tabs
    nav_jobs: "Jobs",
    nav_my_apps: "Applications",
    nav_cabinet: "Dashboard",
    nav_my_posts: "My Jobs",
    nav_post_job: "Post Job"
  }
};

export const normalizeLang = (code) => {
  if (!code) return 'uz';
  const c = String(code).toLowerCase().trim();
  if (c === 'kr' || c === 'oz' || c === 'cyrillic' || c === 'ўз') return 'oz';
  if (c === 'ru' || c === 'rus') return 'ru';
  if (c === 'en' || c === 'eng') return 'en';
  return 'uz';
};
