# buffett_academy_engine.py
"""
==============================================================================
ANGKOR QUANT - FIDUCIARY ACADEMY & WARREN BUFFETT 12 BOOKS MASTERY ENGINE
==============================================================================
Institutional Quantitative Value Investing & Anti-Gambling Education System
Spec: AQ72 (Warren Buffett Fiduciary Curriculum & Quantitative Valuation Suite)

Transforms beginners into disciplined, mathematically grounded quantitative
investors through Warren Buffett's 12 canonical books, eliminating the Zero-Sum
Gambling Trap and instilling long-term compounding principles.

Curriculum Structure (4 Tiers / 12 Lessons):
- Tier 1: White Belt (ថ្នាក់គ្រឹះមូលដ្ឋាន) - Mindset & Zero-Sum Trap Shield (Books 1, 6, 7)
- Tier 2: Green Belt (ថ្នាក់វិភាគគណនេយ្យ) - Financial Forensics & Moat Engineering (Books 2, 8, 3)
- Tier 3: Brown Belt (ថ្នាក់បែងចែកទុន & ចិត្តវិទ្យា) - Capital Allocation & Inversion (Books 4, 5, 11, 12)
- Tier 4: Black Belt (ថ្នាក់វិស្វករវិនិយោគបរិមាណកំពូល) - Algorithmic Value & Snowball Compounding (Books 9, 10 + Quant Engine)
==============================================================================
"""

import time
import math
import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple
import ui_standards

# ==============================================================================
# CANONICAL 12 BUFFETT BOOKS CURRICULUM DIRECTORY
# ==============================================================================

ACADEMY_TIERS = {
    "tier_1": {
        "id": "tier_1",
        "name_km": "ថ្នាក់គ្រឹះមូលដ្ឋាន (White Belt)",
        "name_en": "Foundations & Anti-Gambling Shield",
        "badge": "🥋 សខ្សែក្រវាត់ស",
        "desc_km": "កសាងផ្នត់គំនិតវិនិយោគិនពិតប្រាកដ កម្ចាត់អន្ទាក់ល្បែងស៊ីសង និងយល់ដឹងពីថាមពលការប្រាក់បង្កើនផល (Snowball Compounding)",
        "lessons": [1, 2, 3]
    },
    "tier_2": {
        "id": "tier_2",
        "name_km": "ថ្នាក់វិភាគគណនេយ្យ (Green Belt)",
        "name_en": "Financial Forensics & Moat Engineering",
        "badge": "🥋 ខ្សែក្រវាត់បៃតង",
        "desc_km": "អានរបាយការណ៍ហិរញ្ញវត្ថុដូចជាអ្នកស៊ើបអង្កេត ស្វែងរកក្រុមហ៊ុនមានកំពែងការពារសេដ្ឋកិច្ច (Economic Moat) និងលុបបំបាត់ការបន្លំតួលេខ",
        "lessons": [4, 5, 6]
    },
    "tier_3": {
        "id": "tier_3",
        "name_km": "ថ្នាក់បែងចែកទុន & ចិត្តវិទ្យា (Brown Belt)",
        "name_en": "Capital Allocation & Mental Inversion",
        "badge": "🥋 ខ្សែក្រវាត់ត្នោត",
        "desc_km": "សិល្បៈនៃការបែងចែកទុន (Capital Allocation), ការគិតបញ្ច្រាសទិសរបស់ Charlie Munger និងការគ្រប់គ្រងហានិភ័យមិនស៊ីមេទ្រី",
        "lessons": [7, 8, 9, 10]
    },
    "tier_4": {
        "id": "tier_4",
        "name_km": "ថ្នាក់វិស្វករវិនិយោគបរិមាណកំពូល (Black Belt)",
        "name_en": "Algorithmic Value & Fiduciary Master",
        "badge": "🥋 ខ្សែក្រវាត់ខ្មៅ",
        "desc_km": "សំយោគគោលការណ៍ទាំង ១២ ចូលក្នុងប្រព័ន្ធស្វ័យប្រវត្តិកម្ម Angkor Quant: គណនា DCF, Owner Earnings, Kelly Criterion & Zero Negligence",
        "lessons": [11, 12]
    }
}

ACADEMY_LESSONS: Dict[int, Dict[str, Any]] = {
    1: {
        "id": 1,
        "tier": "tier_1",
        "book_title": "The Intelligent Investor",
        "author": "Benjamin Graham",
        "year": 1949,
        "title_km": "មេរៀនទី ១៖ វិនិយោគិនឆ្លាតវៃ & តួអង្គលោកផ្សារ (Mr. Market)",
        "title_en": "Lesson 1: The Intelligent Investor & Mr. Market",
        "core_thesis": "ការវិនិយោគពិត គឺទិញចំណែកអាជីវកម្ម មិនមែនលេងល្បែងភ្នាល់ថ្លៃឡើងចុះនៃក្រដាសភាគហ៊ុនឡើយ។",
        "fiduciary_pillar": "Margin of Safety (គម្លាតសុវត្ថិភាព) & Emotional Discipline",
        "content_km": (
            "📖 សៀវភៅគោល៖ The Intelligent Investor ដោយលោក Benjamin Graham (គ្រូរបស់ Warren Buffett)\n\n"
            "១. ភាពខុសគ្នារវាង 'ការវិនិយោគ' (Investing) និង 'ល្បែងស៊ីសង' (Speculation/Gambling):\n"
            "   • ការវិនិយោគ៖ គឺជាប្រតិបត្តិការដែលផ្អែកលើការវិភាគស៊ីជម្រៅ ធានាសុវត្ថិភាពដើមទុនជាចម្បង និងទទួលបានផលត្រឡប់សមរម្យ។\n"
            "   • ល្បែងភ្នាល់ (Zero-Sum Trap)៖ គឺការទិញលក់តាមអារម្មណ៍ រំពឹងឱ្យអ្នកបន្ទាប់មកទិញថ្លៃជាងខ្លួន ដោយគ្មានតម្លៃពិតប្រាកដគាំទ្រ។\n\n"
            "២. តួអង្គ 'លោកផ្សារ' (Mr. Market):\n"
            "   • Mr. Market គឺជាដៃគូអាជីវកម្មដែលកើតជំងឺផ្លូវចិត្ត (Manic-Depressive)។ ថ្ងៃខ្លះគាត់រំភើបជ្រុល មកលក់ឱ្យយើងថ្លៃហួសហេតុ។ ថ្ងៃខ្លះគាត់ភ័យស្លន់ស្លោ មកលក់ឱ្យយើងថោកដូចកម្ទេចសំរាម។\n"
            "   • ក្បួនដាច់ខាត៖ កុំឱ្យអារម្មណ៍របស់ Mr. Market មកដឹកនាំការសម្រេចចិត្តរបស់យើង! ចូរឆ្លៀតឱកាសពីភាពភ័យខ្លាចរបស់គាត់ ដើម្បីទិញទ្រព្យល្អក្នុងតម្លៃថោក។\n\n"
            "៣. គម្លាតសុវត្ថិភាព (Margin of Safety):\n"
            "   • បើយើងសង់ស្ពានសម្រាប់ឡានទម្ងន់ ១០ តោនឆ្លងកាត់ យើងត្រូវសង់ស្ពានដែលទ្រទម្ងន់បាន ៣០ តោន។\n"
            "   • ក្នុងការវិនិយោគ បើតម្លៃពិត (Intrinsic Value) ស្មើ $100 យើងត្រូវទិញនៅតម្លៃ $60-$70 ចុះក្រោម។ បើយើងគណនាខុសបន្តិច ក៏នៅតែមិនខាតបង់ដើមទុន!"
        ),
        "formula": "Margin of Safety = (Intrinsic Value - Market Price) / Intrinsic Value >= 30%",
        "quiz": {
            "question": "តើតួអង្គ 'Mr. Market' តំណាងឱ្យអ្វីនៅក្នុងទីផ្សារហិរញ្ញវត្ថុ?",
            "options": [
                "A) មេខ្យល់ដែលតែងតែកំណត់តម្លៃត្រឹមត្រូវឥតខ្ចោះជានិច្ច",
                "B) ដៃគូដែលប្រែប្រួលតាមអារម្មណ៍រំភើប និងភ័យខ្លាច ដែលយើងត្រូវឆ្លៀតឱកាសទាញចំណេញ មិនមែនធ្វើតាមគាត់ទេ",
                "C) ក្បួនកាត់ខាតស្វ័យប្រវត្តិតាមបច្ចេកទេស"
            ],
            "correct_index": 1,
            "explanation": "Mr. Market តែងតែមានអារម្មណ៍ឡើងចុះជ្រុល (Manic-Depressive)។ វិនិយោគិនឆ្លាតវៃទាញប្រយោជន៍ពីភាពភ័យខ្លាចរបស់គាត់ ដើម្បីទិញទ្រព្យល្អក្នុងតម្លៃទាប មិនមែនស្លន់ស្លោតាមគាត់ឡើយ!"
        }
    },
    2: {
        "id": 2,
        "tier": "tier_1",
        "book_title": "The Snowball: Warren Buffett and the Business of Life",
        "author": "Alice Schroeder",
        "year": 2008,
        "title_km": "មេរៀនទី ២៖ ដុំព្រិលវិលបង្កើនផល (The Snowball) & រង្វង់ជំនាញ",
        "title_en": "Lesson 2: The Snowball Compounding & Circle of Competence",
        "core_thesis": "ជីវិត និងទ្រព្យសម្បត្តិ គឺដូចជាដុំព្រិល។ អ្វីដែលអ្នកត្រូវការគឺព្រិលដែលសើម និងជម្រាលភ្នំដ៏វែងអន្លាយ។",
        "fiduciary_pillar": "Compound Interest, Circle of Competence & Inner Scorecard",
        "content_km": (
            "📖 សៀវភៅគោល៖ The Snowball ដោយ Alice Schroeder\n\n"
            "១. ថាមពលនៃអព្ភូតហេតុទី ៨ (Compound Interest):\n"
            "   • Warren Buffett រកបានទ្រព្យសម្បត្តិជាង ៩៩% បន្ទាប់ពីគាត់មានអាយុ ៥០ ឆ្នាំ។ អាថ៌កំបាំងមិនមែនត្រឹមតែការរកប្រាក់ចំណេញខ្ពស់ក្នុងមួយថ្ងៃនោះទេ គឺស្ថិតលើ 'ការមិនខាតបង់' និង 'ការបណ្តោយឱ្យផលចំណេញកើនឡើងតាមពេលវេលាដ៏យូរ'។\n\n"
            "២. រង្វង់នៃសមត្ថភាព (Circle of Competence):\n"
            "   • អ្នកមិនចាំបាច់ជាអ្នកជំនាញគ្រប់វិស័យឡើយ។ អ្វីដែលសំខាន់បំផុត គឺត្រូវដឹងច្បាស់ថាព្រំដែននៃចំណេះដឹងរបស់អ្នកនៅត្រង់ណា ហើយដាច់ខាតកុំឈានជើងចេញក្រៅព្រំដែននោះ។\n"
            "   • ការដឹងពីអ្វីដែលយើងមិនចេះ គឺមានតម្លៃជាងការមានភាពវៃឆ្លាតទៅទៀត។\n\n"
            "៣. បន្ទាត់វាស់វែងខាងក្នុង (Inner Scorecard vs Outer Scorecard):\n"
            "   • Outer Scorecard: ខ្វល់តែពីក្រសែភ្នែកអ្នកដទៃគិតមកលើយើង (ការអួតសម្ភារៈ ជោគជ័យបណ្តោះអាសន្នលើល្បែង)។\n"
            "   • Inner Scorecard: វិនិច្ឆ័យខ្លួនឯងលើសច្ចភាព វិន័យ និងការគោរពគោលការណ៍វិស្វកម្ម ទោះបីពិភពលោកទាំងមូលយល់ច្រឡំក៏ដោយ។"
        ),
        "formula": "Future Value = Present Value * (1 + r)^n | n = ចំនួនឆ្នាំនៃការបង្កើនផលយូរអង្វែង",
        "quiz": {
            "question": "តើអ្វីជាកត្តាសំខាន់បំផុតក្នុងការធ្វើឱ្យដុំព្រិលហិរញ្ញវត្ថុ (Snowball) កាន់តែរីកធំ?",
            "options": [
                "A) ការលេងភ្នាល់ Leverage 50x-100x ឱ្យចំណេញរហ័សក្នុងមួយយប់",
                "B) ពេលវេលាវិនិយោគដ៏វែងអន្លាយ និងការការពារដើមទុនមិនឱ្យបាត់បង់ (Rule #1)",
                "C) ការទិញលក់ចេញចូលរាល់ម៉ោងតាមព័ត៌មានទូរទស្សន៍"
            ],
            "correct_index": 1,
            "explanation": "ដុំព្រិល Snowball ត្រូវការជម្រាលភ្នំវែង (ពេលវេលា) និងការមិនបែកបាក់ដុំព្រិល (មិនខាតបង់ដើមទុនធ្ងន់ធ្ងរ)។ ការលេង Leverage ខ្ពស់នឹងបំបែកដុំព្រិលឱ្យរលាយបាត់ភ្លាមៗ!"
        }
    },
    3: {
        "id": 3,
        "tier": "tier_1",
        "book_title": "Tap Dancing to Work",
        "author": "Carol Loomis",
        "year": 2012,
        "title_km": "មេរៀនទី ៣៖ សេចក្តីស្មោះត្រង់វិជ្ជាជីវៈ (Fiduciary Integrity) & ភាពរីករាយក្នុងការងារ",
        "title_en": "Lesson 3: Tap Dancing to Work & Fiduciary Stewardship",
        "core_thesis": "កេរ្តិ៍ឈ្មោះត្រូវការពេល ២០ ឆ្នាំដើម្បីកសាង ប៉ុន្តែអាចត្រូវបំផ្លាញត្រឹមតែ ៥ នាទីប៉ុណ្ណោះ។",
        "fiduciary_pillar": "Ethical Stewardship, Skin in the Game & Avoiding Ruinous Debt",
        "content_km": (
            "📖 សៀវភៅគោល៖ Tap Dancing to Work ដោយ Carol Loomis\n\n"
            "១. កាតព្វកិច្ច Fiduciary Duty (ការការពារផលប្រយោជន៍អ្នកវិនិយោគជាធំ):\n"
            "   • Warren Buffett ចាត់ទុកម្ចាស់ភាគហ៊ុន Berkshire Hathaway ទាំងអស់ជាដៃគូរួមសុខទុក្ខ មិនមែនជាអតិថិជនដើម្បីកេងចំណេញកម្រៃជើងសារឡើយ។\n"
            "   • នៅក្នុង Angkor Quant យើងប្រកាន់ខ្ជាប់នូវ Fiduciary Refusal: បដិសេធដាច់ខាតមិនអនុវត្តកូដ ឬយុទ្ធសាស្ត្របំផ្លាញដើមទុន (ដូចជា Martingale ឬ No-SL) ទោះបីជាមានការស្នើសុំក៏ដោយ។\n\n"
            "២. គ្រោះថ្នាក់នៃបំណុល និង Leverage (Ruinous Leverage):\n"
            "   • បំណុលគឺជាឧបករណ៍តែមួយគត់ដែលអាចធ្វើឱ្យមនុស្សឆ្លាតវៃក្ស័យធនបាន។\n"
            "   • ប្រសិនបើអ្នកឆ្លាត អ្នកមិនត្រូវការ Leverage ខ្ពស់ទេ។ ប្រសិនបើអ្នកមិនឆ្លាត ការប្រើ Leverage នឹងនាំអ្នកទៅរកសេចក្តីវិនាសកាន់តែលឿន!\n\n"
            "៣. ស្រឡាញ់ការងារដែលខ្លួនធ្វើ (Tap Dance to Work):\n"
            "   • វិនិយោគិនពិតប្រាកដ រីករាយនឹងការវិភាគ ការកសាងប្រព័ន្ធ និងការបង្កើតតម្លៃពិត មិនមែនអង្គុយភ័យតក់ស្លុតនឹងអេក្រង់តម្លៃនោះឡើយ។"
        ),
        "formula": "Fiduciary Edge = Mathematical Expectancy > 0 AND Leverage <= Safe Cap",
        "quiz": {
            "question": "យោងតាមលោក Warren Buffett តើអ្វីជាគ្រោះថ្នាក់ចម្បងបំផុតនៃការប្រើប្រាស់បំណុល ឬ Leverage ខ្ពស់?",
            "options": [
                "A) វានាំឱ្យមនុស្សឆ្លាតវៃប្រឈមនឹងការដាច់ខាតដើមទុនទាំងស្រុង នៅពេលទីផ្សារប្រែប្រួលមួយភ្លែត",
                "B) វាមិនមានផលប៉ះពាល់អ្វីទេ ប្រសិនបើយើងមានទំនុកចិត្តលើខ្លួនឯង",
                "C) វាជួយកាត់បន្ថយថ្លៃ Spread របស់ឈ្មួញកណ្តាល"
            ],
            "correct_index": 0,
            "explanation": "Leverage ខ្ពស់ដកហូតពេលវេលារបស់អ្នក។ ទោះបីការវិភាគរយៈពេលវែងរបស់អ្នកត្រឹមត្រូវ ក៏ការប្រែប្រួលរលកបណ្តោះអាសន្ននឹង thanh lý (liquidate) ដើមទុនរបស់អ្នករលីង!"
        }
    },
    4: {
        "id": 4,
        "tier": "tier_2",
        "book_title": "Security Analysis",
        "author": "Benjamin Graham & David Dodd",
        "year": 1934,
        "title_km": "មេរៀនទី ៤៖ កោសល្យវិច័យរបាយការណ៍ហិរញ្ញវត្ថុ & តម្លៃពិតអាជីវកម្ម",
        "title_en": "Lesson 4: Security Analysis & Balance Sheet Forensics",
        "core_thesis": "ការវិភាគមូលបត្រ គឺស្វែងរកការពិតដែលលាក់នៅពីក្រោយតួលេខគណនេយ្យ។",
        "fiduciary_pillar": "Net Current Asset Value (NCAV), Liquidation Value & Earnings Power",
        "content_km": (
            "📖 សៀវភៅគោល៖ Security Analysis (គម្ពីរដើមនៃការវិភាគមូលបត្រ) ដោយ Graham & Dodd\n\n"
            "១. ការពិនិត្យតារាងតុល្យការ (Balance Sheet Forensics):\n"
            "   • ទ្រព្យសកម្ម (Assets) មិនមែនសុទ្ធតែមានតម្លៃស្មើនឹងអ្វីដែលសរសេរលើក្រដាសនោះទេ។ សន្និធិ (Inventory) និងបំណុលត្រូវទារ (Accounts Receivable) អាចនឹងត្រូវបញ្ចុះតម្លៃយ៉ាងគំហុកនៅពេលមានវិបត្តិ។\n"
            "   • ស្វែងរកក្រុមហ៊ុនដែលមានសាច់ប្រាក់សុទ្ធច្រើន និងបំណុលរយៈពេលខ្លីទាប។\n\n"
            "២. តម្លៃទ្រព្យសកម្មចរន្តសុទ្ធ (Net Current Asset Value - NCAV / Net-Net):\n"
            "   • រូបមន្ត Graham Net-Net: ទ្រព្យសកម្មចរន្ត ដកបំណុលសរុបទាំងអស់។ ប្រសិនបើតម្លៃទីផ្សាររបស់ក្រុមហ៊ុនទាបជាង NCAV នោះគឺជាឱកាសទិញដោយឥតគិតថ្លៃរោងចក្រ និងម៉ាស៊ីន!\n\n"
            "៣. សមត្ថភាពរកចំណូលប្រកបដោយចីរភាព (Earnings Power):\n"
            "   • កុំមើលតែប្រាក់ចំណេញត្រឹមមួយត្រីមាស ឬមួយឆ្នាំ។ ចូរពិនិត្យមើលមធ្យមភាគប្រាក់ចំណូលរយៈពេល ៥ ទៅ ១០ ឆ្នាំ ឆ្លងកាត់ទាំងរដូវកាលសេដ្ឋកិច្ចរីកចម្រើន និងវិបត្តិ។"
        ),
        "formula": "NCAV = Current Assets - Total Liabilities - Preferred Stock",
        "quiz": {
            "question": "តើទ្រព្យសកម្មចរន្តសុទ្ធ (NCAV) ត្រូវបានគណនាដូចម្តេច?",
            "options": [
                "A) ទ្រព្យសកម្មអចលនទ្រព្យ បូកនឹងកេរ្តិ៍ឈ្មោះក្រុមហ៊ុន (Goodwill)",
                "B) ទ្រព្យសកម្មចរន្ត (Current Assets) ដកចេញនូវបំណុលសរុបទាំងអស់ (Total Liabilities)",
                "C) ប្រាក់ចំណេញសុទ្ធ គុណនឹងអត្រាកំណើនប្រចាំឆ្នាំ"
            ],
            "correct_index": 1,
            "explanation": "NCAV = Current Assets - Total Liabilities។ នេះជាទ្រព្យសម្បត្តិរាវសុទ្ធដែលនៅសល់ ប្រសិនបើក្រុមហ៊ុនត្រូវទូទាត់បំណុលទាំងអស់ភ្លាមៗ!"
        }
    },
    5: {
        "id": 5,
        "tier": "tier_2",
        "book_title": "Warren Buffett and the Interpretation of Financial Statements",
        "author": "Mary Buffett & David Clark",
        "year": 2008,
        "title_km": "មេរៀនទី ៥៖ សម្គាល់កំពែងសេដ្ឋកិច្ច (Economic Moat) តាមរបាយការណ៍ហិរញ្ញវត្ថុ",
        "title_en": "Lesson 5: Identifying Durable Economic Moats in Financials",
        "core_thesis": "ក្រុមហ៊ុនដែលមានកំពែងសេដ្ឋកិច្ចរឹងមាំ តែងតែបន្សល់ទុកនូវស្នាមជើងតួលេខដ៏ពិសេសនៅក្នុងរបាយការណ៍ហិរញ្ញវត្ថុ។",
        "fiduciary_pillar": "Gross Margin > 40%, Low CapEx/Net Income, High Return on Equity (ROE)",
        "content_km": (
            "📖 សៀវភៅគោល៖ Interpretation of Financial Statements ដោយ Mary Buffett & David Clark\n\n"
            "១. សូចនាកររក្សាកំពែងសេដ្ឋកិច្ច (Durable Moat Benchmarks):\n"
            "   • ផលចំណេញដុល (Gross Margin) > 40%៖ បង្ហាញថាក្រុមហ៊ុនមានអំណាចក្នុងការកំណត់ថ្លៃ (Pricing Power) និងគ្មានគូប្រជែងណាដណ្តើមបានងាយៗឡើយ។\n"
            "   • ចំណាយលក់ និងរដ្ឋបាល (SGA / Gross Profit) < 30%៖ ការគ្រប់គ្រងចំណាយមានប្រសិទ្ធភាពខ្ពស់។\n"
            "   • ចំណាយការប្រាក់ (Interest Expense / Operating Income) < 15%៖ បង្ហាញថាក្រុមហ៊ុនមិនពឹងផ្អែកលើបំណុលធ្ងន់ធ្ងរដើម្បីរស់។\n\n"
            "២. ការវិនិយោគដើមទុនថែទាំ (CapEx Efficiency):\n"
            "   • ក្រុមហ៊ុនដែលមានកំពែងរឹងមាំ ចំណាយ CapEx មិនលើសពី 25% ទៅ 50% នៃប្រាក់ចំណេញសុទ្ធប្រចាំឆ្នាំឡើយ។ ផ្ទុយទៅវិញ ក្រុមហ៊ុនគ្មានកំពែង (ដូចជាក្រុមហ៊ុនអាកាសចរណ៍) ត្រូវបូមសាច់ប្រាក់ស្ទើរតែទាំងអស់ទៅទិញយន្តហោះថ្មីជានិច្ច។\n\n"
            "៣. ផលត្រឡប់លើមូលធនផ្ទាល់ (Return on Equity - ROE > 15-20%):\n"
            "   • ក្រុមហ៊ុនដែលរកចំណូលបានខ្ពស់លើដើមទុនរបស់ម្ចាស់ភាគហ៊ុន ដោយមិនបាច់ពឹងផ្អែកលើបំណុលខ្ពស់ គឺជាម៉ាស៊ីនបង្កើតទ្រព្យសម្បត្តិដ៏ពិតប្រាកដ។"
        ),
        "formula": "Durable Moat Score = (Gross Margin > 40%) + (SGA < 35%) + (CapEx/NI < 30%) + (ROE > 15%)",
        "quiz": {
            "question": "តើសូចនាករណាមួយបង្ហាញថាក្រុមហ៊ុនមានអំណាចកំណត់ថ្លៃ (Pricing Power) និងកំពែងសេដ្ឋកិច្ចរឹងមាំ?",
            "options": [
                "A) ផលចំណេញដុល (Gross Margin) ស្ថិតនៅកម្រិតខ្ពស់ជាប់លាប់លើសពី 40%",
                "B) បំណុលរយៈពេលវែងកើនឡើង 100% ជារៀងរាល់ឆ្នាំ",
                "C) ការចំណាយលើយុទ្ធនាការផ្សាយពាណិជ្ជកម្មច្រើនជាងចំណូលលក់"
            ],
            "correct_index": 0,
            "explanation": "Gross Margin > 40% ជាប់លាប់ច្រើនឆ្នាំ បញ្ជាក់ថាក្រុមហ៊ុនអាចលក់ផលិតផលបានថ្លៃជាងថ្លៃដើមផលិតយ៉ាងច្រើន ដោយអតិថិជននៅតែស្ម័គ្រចិត្តទិញ ព្រោះគ្មានជម្រើសជំនួសល្អជាង!"
        }
    },
    6: {
        "id": 6,
        "tier": "tier_2",
        "book_title": "Common Stocks and Uncommon Profits",
        "author": "Philip Fisher",
        "year": 1958,
        "title_km": "មេរៀនទី ៦៖ វិធីសាស្ត្រស៊ើបអង្កេត Scuttlebutt & កំណើនប្រកបដោយគុណភាព",
        "title_en": "Lesson 6: The Scuttlebutt Method & High-Quality Growth",
        "core_thesis": "ការវិនិយោគលើក្រុមហ៊ុនល្អឥតខ្ចោះ ក្នុងតម្លៃសមរម្យ គឺប្រសើរជាងការទិញក្រុមហ៊ុនអន់ក្នុងតម្លៃថោក។",
        "fiduciary_pillar": "Fisher's 15 Points, Qualitative Edge & Long-Term Compounding",
        "content_km": (
            "📖 សៀវភៅគោល៖ Common Stocks and Uncommon Profits ដោយ Philip Fisher\n\n"
            "១. ការផ្លាស់ប្តូរផ្នត់គំនិតរបស់ Warren Buffett (85% Graham + 15% Fisher):\n"
            "   • Graham បង្រៀនឱ្យទិញ 'កន្ទុយបារី' (Cigar Butts) ដែលគេបោះចោលដើម្បីជក់មួយបង្ហុយឥតគិតថ្លៃ។ ប៉ុន្តែ Fisher បានបង្រៀនឱ្យទិញ 'ក្រុមហ៊ុនកំពូល' (Wonderful Businesses) ដែលមានការរីកចម្រើនមិនចេះចប់។\n\n"
            "២. វិធីសាស្ត្រស៊ើបអង្កេតក្រៅផ្លូវការ (The Scuttlebutt Method):\n"
            "   • កុំជឿតែអ្វីដែលថ្នាក់ដឹកនាំនិយាយនៅក្នុងកិច្ចប្រជុំ! ចូរទៅសាកសួរអតិថិជន អ្នកផ្គត់ផ្គង់ (Suppliers) បុគ្គលិកចាស់ និងគូប្រជែងផ្ទាល់ ដើម្បីដឹងពីការពិតនៃគុណភាពផលិតផល និងភាពស្មោះត្រង់របស់ក្រុមហ៊ុន។\n\n"
            "៣. ការស្រាវជ្រាវ និងអភិវឌ្ឍន៍ (R&D Effectiveness):\n"
            "   • ក្រុមហ៊ុនដែលវិនិយោគលើការស្រាវជ្រាវផលិតផលថ្មីប្រកបដោយប្រសិទ្ធភាពខ្ពស់ នឹងបង្កើតប្រភពចំណូលថ្មីៗជាបន្តបន្ទាប់សម្រាប់អនាគត។"
        ),
        "formula": "High-Quality Multiplier = High ROIC * Reinvestment Rate",
        "quiz": {
            "question": "តើវិធីសាស្ត្រ 'Scuttlebutt' របស់ Philip Fisher ផ្តោតសំខាន់លើអ្វី?",
            "options": [
                "A) ការមើលក្រាហ្វបច្ចេកទេស និងបន្ទាត់ Moving Average 1 នាទី",
                "B) ការប្រមូលព័ត៌មានជាក់ស្តែងពីអតិថិជន អ្នកផ្គត់ផ្គង់ និងគូប្រជែងដើម្បីវាយតម្លៃគុណភាពអាជីវកម្ម",
                "C) ការទិញលក់ភាគហ៊ុនតាមពាក្យចចាមអារ៉ាមនៅលើបណ្តាញសង្គម"
            ],
            "correct_index": 1,
            "explanation": "Scuttlebutt គឺជាការស៊ើបអង្កេត 360 ដឺក្រេជាក់ស្តែងជុំវិញអាជីវកម្ម ដើម្បីបញ្ជាក់ថាផលិតផល និងសេវាកម្មពិតជាទទួលបានការពេញចិត្តពីទីផ្សារពិតប្រាកដឬអត់!"
        }
    },
    7: {
        "id": 7,
        "tier": "tier_3",
        "book_title": "The Essays of Warren Buffett",
        "author": "Warren Buffett & Lawrence Cunningham",
        "year": 1997,
        "title_km": "មេរៀនទី ៧៖ ប្រាក់ចំណូលពិតរបស់ម្ចាស់អាជីវកម្ម (Owner Earnings) & ការបែងចែកទុន",
        "title_en": "Lesson 7: Owner Earnings & Master Capital Allocation",
        "core_thesis": "ប្រាក់ចំណេញគណនេយ្យ (Net Income) អាចត្រូវគេបន្លំបាន ប៉ុន្តែសាច់ប្រាក់ពិតរបស់ម្ចាស់ (Owner Earnings) មិនកុហកឡើយ។",
        "fiduciary_pillar": "Owner Earnings Formula, Look-Through Earnings & Capital Allocation",
        "content_km": (
            "📖 សៀវភៅគោល៖ The Essays of Warren Buffett ដោយ Lawrence Cunningham\n\n"
            "១. រូបមន្តគណនាប្រាក់ចំណូលម្ចាស់ (Owner Earnings - សំបុត្រឆ្នាំ ១៩៨៦):\n"
            "   • Owner Earnings = ប្រាក់ចំណេញសុទ្ធ (Net Income) + រំលស់ (Depreciation & Amortization) - ដើមទុនថែទាំទ្រព្យ (Maintenance CapEx) +/- បំរែបំរួលទុនបង្វិល (Working Capital Changes)។\n"
            "   • នេះជាសាច់ប្រាក់សុទ្ធដែលម្ចាស់អាជីវកម្មអាចដកយកមកប្រើប្រាស់ផ្ទាល់ខ្លួនបាន ដោយមិនធ្វើឱ្យប៉ះពាល់ដល់សមត្ថភាពប្រកួតប្រជែងរបស់ក្រុមហ៊ុនឡើយ។\n\n"
            "២. ការបែងចែកទុន (Capital Allocation - តួនាទីសំខាន់បំផុតរបស់ CEO):\n"
            "   • នៅពេលក្រុមហ៊ុនរកប្រាក់ចំណេញបាន តើគួរយកទៅណា?\n"
            "     ១. វិនិយោគឡើងវិញក្នុងអាជីវកម្ម (បើ ROIC > Cost of Capital)\n"
            "     ២. ទិញក្រុមហ៊ុនផ្សេងទៀតដែលមានកំពែងសេដ្ឋកិច្ច\n"
            "     ៣. ទិញភាគហ៊ុនខ្លួនឯងមកវិញ (Share Buyback) នៅពេលតម្លៃភាគហ៊ុនធ្លាក់ថោកជាងតម្លៃពិត\n"
            "     ៤. ចែកភាគលាភ (Dividends)\n"
            "     ៥. សងបំណុល\n\n"
            "៣. ភាគហ៊ុនជាចំណែកនៃអាជីវកម្ម (Look-Through Earnings):\n"
            "   • កុំរំភើបតែពេលតម្លៃភាគហ៊ុនឡើង ចូរគិតពីចំណែកនៃប្រាក់ចំណេញដែលក្រុមហ៊ុនកំពុងរកបានជំនួសយើងជារៀងរាល់ថ្ងៃ។"
        ),
        "formula": "Owner Earnings = Net Income + D&A - Maintenance CapEx +/- Working Capital Change",
        "quiz": {
            "question": "ហេតុអ្វីបានជា Warren Buffett ចូលចិត្តប្រើ 'Owner Earnings' ជាង 'Net Income' ធម្មតា?",
            "options": [
                "A) ព្រោះវាឆ្លុះបញ្ចាំងពីសាច់ប្រាក់ពិតប្រាកដដែលនៅសល់ បន្ទាប់ពីកាត់ចេញនូវការចំណាយថែទាំទ្រព្យសកម្មចាស់ៗ",
                "B) ព្រោះវាធ្វើឱ្យតួលេខប្រាក់ចំណេញមើលទៅធំជាងមុនសម្រាប់បង់ពន្ធតិច",
                "C) ព្រោះវាងាយស្រួលគណនាដោយមិនបាច់មើលរបាយការណ៍ហិរញ្ញវត្ថុ"
            ],
            "correct_index": 0,
            "explanation": "Net Income មិនបានគិតដល់សាច់ប្រាក់ដែលត្រូវបង្ខំចិត្តយកទៅទិញគ្រឿងចក្រថ្មីដើម្បីថែទាំអាជីវកម្មនោះទេ។ Owner Earnings បង្ហាញសាច់ប្រាក់សេរីពិតប្រាកដដែលម្ចាស់អាចដកបាន!"
        }
    },
    8: {
        "id": 8,
        "tier": "tier_3",
        "book_title": "Poor Charlie's Almanack",
        "author": "Charles T. Munger & Peter Kaufman",
        "year": 2005,
        "title_km": "មេរៀនទី ៨៖ គំរូផ្នត់គំនិតពហុជំនាញ (Mental Models) & ក្បួនគិតបញ្ច្រាស (Inversion)",
        "title_en": "Lesson 8: Mental Models & The Power of Inversion",
        "core_thesis": "ចូរប្រាប់ខ្ញុំថាកន្លែងណាដែលខ្ញុំនឹងស្លាប់ នោះខ្ញុំនឹងមិនទៅទីនោះដាច់ខាត។",
        "fiduciary_pillar": "Inversion Principle, Lollapalooza Effect & Cognitive Bias Removal",
        "content_km": (
            "📖 សៀវភៅគោល៖ Poor Charlie's Almanack ដោយលោក Charlie Munger (ដៃគូដួងចិត្ត Buffett)\n\n"
            "១. គោលការណ៍គិតបញ្ច្រាស (Invert, Always Invert):\n"
            "   • បើចង់ដឹងពីរបៀបជោគជ័យក្នុងការវិនិយោគ ចូរសួរខ្លួនឯងជាមុនសិនថា៖ 'តើអ្វីខ្លះដែលធ្វើឱ្យវិនិយោគិនវិនាសដើមទុន?' បន្ទាប់មកចៀសវាងរឿងទាំងនោះឱ្យដាច់ខាត!\n"
            "   • អ្វីដែលបំផ្លាញដើមទុន៖ ការលោភលន់ប្រើ Leverage ខ្ពស់, ការទិញទ្រព្យដែលខ្លួនមិនយល់, ការគ្មាន Stop-Loss, ការលេងតាមអារម្មណ៍។\n\n"
            "២. បណ្តាញនៃគំរូផ្នត់គំនិតពហុជំនាញ (Lattice of Mental Models):\n"
            "   • បើអ្នកមានតែកូនញញួរមួយក្នុងដៃ អ្នកនឹងមើលឃើញបញ្ហាគ្រប់យ៉ាងដូចជាដែកគោល។\n"
            "   • វិនិយោគិនកំពូលត្រូវយល់ដឹងពី គណិតវិទ្យា (ប្រូបាប៊ីលីតេ), ចិត្តវិទ្យា (ការលម្អៀងខាងការយល់ដឹង), ជីវវិទ្យា (ការវិវត្តន៍), និងរូបវិទ្យា (កម្លាំងរុញច្រាន)។\n\n"
            "៣. បាតុភូត Lollapalooza Effect:\n"
            "   • នៅពេលកត្តាចិត្តវិទ្យាខុសឆ្គងជាច្រើន (ដូចជា FOMO + Social Proof + Sunk Cost Fallacy) មកជួបគ្នាដំណាលគ្នា វានឹងបង្កើតជាមហន្តរាយហិរញ្ញវត្ថុដ៏ធំធេង (ដូចជា Bubble & Crash)។"
        ),
        "formula": "Survival Rate = 1 - P(Critical Structural Mistake)",
        "quiz": {
            "question": "តើក្បួន 'Inversion' (គិតបញ្ច្រាស) របស់ Charlie Munger ត្រូវបានអនុវត្តក្នុងការគ្រប់គ្រងហានិភ័យយ៉ាងដូចម្តេច?",
            "options": [
                "A) ស្វែងរកវិធីកម្ចាត់ចំណុចខ្សោយ និងបញ្ចៀសសកម្មភាពដែលនាំទៅរកសេចក្តីវិនាសជាមុនសិន",
                "B) ដាក់បញ្ជា Sell គ្រប់ពេលដែលទីផ្សារឡើងថ្លៃ",
                "C) បង្កើនទំហំជួញដូរទ្វេដងនៅពេលខាតបង់ (Martingale)"
            ],
            "correct_index": 0,
            "explanation": "Inversion បង្រៀនឱ្យយើងកំណត់ឱ្យច្បាស់នូវរាល់កំហុសឆ្គងបច្ចេកទេស និងផ្លូវចិត្តដែលតែងតែសម្លាប់ដើមទុន ហើយចាក់សោរបញ្ចៀសវា ១០០% ជាមុន មុននឹងគិតពីប្រាក់ចំណេញ!"
        }
    },
    9: {
        "id": 9,
        "tier": "tier_3",
        "book_title": "The Most Important Thing",
        "author": "Howard Marks",
        "year": 2011,
        "title_km": "មេរៀនទី ៩៖ ការគិតកម្រិតទីពីរ (Second-Level Thinking) & វដ្តទីផ្សារ",
        "title_en": "Lesson 9: Second-Level Thinking & Navigating Market Cycles",
        "core_thesis": "ការគ្រប់គ្រងហានិភ័យ មិនមែនមើលឃើញនៅពេលទីផ្សារឡើងនោះទេ គឺមើលឃើញនៅពេលទឹកស្រក។",
        "fiduciary_pillar": "Second-Level Thinking, Market Cycles & Asymmetric Risk/Reward",
        "content_km": (
            "📖 សៀវភៅគោល៖ The Most Important Thing ដោយ Howard Marks (សៀវភៅដែល Buffett អានពីរដង)\n\n"
            "១. ការគិតកម្រិតទីមួយ ទល់នឹង កម្រិតទីពីរ (First-Level vs Second-Level Thinking):\n"
            "   • First-Level (អ្នកលេងទូទៅ)៖ 'ក្រុមហ៊ុននេះល្អ ចំណូលកើនឡើង ចូរទិញវា!'\n"
            "   • Second-Level (អ្នកជំនាញបរិមាណ)៖ 'ក្រុមហ៊ុននេះល្អ ប៉ុន្តែមនុស្សគ្រប់គ្នាសុទ្ធតែដឹងរួចហើយ ដូច្នេះតម្លៃទីផ្សារត្រូវបានទិញឡើងថ្លៃហួសហេតុទៅហើយ។ បើមានបញ្ហាបន្តិចបន្តួច វានឹងធ្លាក់ចុះយ៉ាងធ្ងន់ធ្ងរ ដូច្នេះមិនត្រូវទិញឡើយ!'\n\n"
            "២. វដ្តទីផ្សារ (The Pendulum of Market Cycles):\n"
            "   • អារម្មណ៍ទីផ្សារដូចជាប៉ោលនាឡិកា ដែលតែងតែយោលរវាងភាពលោភលន់ហួសហេតុ និងភាពភ័យខ្លាចហួសហេតុ។ វាកម្រឈប់នៅត្រង់ចំណុចកណ្តាលយូរណាស់។\n"
            "   • នៅពេលមនុស្សគ្រប់គ្នាជឿថាមិនមានហានិភ័យ នោះហើយជាពេលដែលហានិភ័យខ្ពស់បំផុត!\n\n"
            "៣. ផលចំណេញមិនស៊ីមេទ្រី (Asymmetric Risk/Reward):\n"
            "   • វិនិយោគិនពូកែ មិនមែនជាអ្នកដែលរកចំណេញបានច្រើនពេលទីផ្សារឡើងនោះទេ គឺរក្សាប្រាក់ចំណេញបានស្ទើរតែទាំងអស់នៅពេលទីផ្សារធ្លាក់ចុះ!"
        ),
        "formula": "Asymmetric Edge: E[R] = (Win Rate * Win Amount) - (Loss Rate * Loss Amount) > Fee Hurdle",
        "quiz": {
            "question": "តើអ្វីជាលក្ខណៈសម្គាល់នៃ 'ការគិតកម្រិតទីពីរ' (Second-Level Thinking)?",
            "options": [
                "A) គិតពិចារណាលើការរំពឹងទុករបស់ទីផ្សារ តម្លៃដែលបានបូកបញ្ចូលរួច (Priced-in) និងប្រូបាប៊ីលីតេនៃហានិភ័យ",
                "B) ធ្វើតាមការណែនាំរបស់មិត្តភក្តិភ្លាមៗដោយមិនបាច់វិភាគ",
                "C) ទិញភាគហ៊ុនណាដែលមានឈ្មោះល្បីបំផុតនៅលើសារព័ត៌មាន"
            ],
            "correct_index": 0,
            "explanation": "Second-level thinking គិតស៊ីជម្រៅជាងធម្មតា៖ វាយតម្លៃថាតើតម្លៃបច្ចុប្បន្នបានឆ្លុះបញ្ចាំងដំណឹងល្អរួចហើយឬនៅ និងអ្វីដែលនឹងកើតឡើងប្រសិនបើតួលេខជាក់ស្តែងមិនដូចការរំពឹងទុក!"
        }
    },
    10: {
        "id": 10,
        "tier": "tier_3",
        "book_title": "The Outsiders",
        "author": "William N. Thorndike",
        "year": 2012,
        "title_km": "មេរៀនទី ១០៖ មេដឹកនាំអាជីវកម្មក្រៅប្រព័ន្ធ (The Outsiders) & ការបែងចែកទុនកំពូល",
        "title_en": "Lesson 10: Unconventional CEOs & Capital Allocation Mastery",
        "core_thesis": "ភាពជោគជ័យយូរអង្វែងរបស់ក្រុមហ៊ុន អាស្រ័យលើរបៀបដែល CEO យកសាច់ប្រាក់ទៅវិនិយោគបន្ត។",
        "fiduciary_pillar": "Share Buybacks at Discount, Decentralized Operations & Per-Share Value",
        "content_km": (
            "📖 សៀវភៅគោល៖ The Outsiders ដោយ William N. Thorndike (សៀវភៅអនុសាសន៍លេខ ១ របស់ Buffett)\n\n"
            "១. លក្ខណៈពិសេសរបស់ CEO កំពូលទាំង ៨ រូប (Unconventional CEOs):\n"
            "   • ពួកគេមិនខ្វល់ពីទំហំក្រុមហ៊ុនឱ្យធំ ឬការឡើងថ្លែងការណ៍លើកញ្ចក់ទូរទស្សន៍ Wall Street ឡើយ។ ពួកគេផ្តោតតែមួយគត់លើ 'កំណើនតម្លៃសាច់ប្រាក់ក្នុងមួយភាគហ៊ុន' (Cash Flow Per Share)។\n\n"
            "២. ការទិញភាគហ៊ុនខ្លួនឯងមកវិញ (Aggressive Share Buybacks):\n"
            "   • នៅពេលទីផ្សារស្លន់ស្លោទម្លាក់ថ្លៃភាគហ៊ុនចុះក្រោមតម្លៃពិត CEO ឆ្លាតវៃនឹងយកសាច់ប្រាក់ក្រុមហ៊ុនទៅទិញភាគហ៊ុនមកវិញ។ នេះធ្វើឱ្យម្ចាស់ភាគហ៊ុនដែលនៅសល់ កើនចំណែកកម្មសិទ្ធិដោយស្វ័យប្រវត្តិដោយមិនបាច់ចំណាយប្រាក់បន្ថែម!\n\n"
            "៣. ការគ្រប់គ្រងបែបវិមជ្ឈការ (Decentralized Autonomy):\n"
            "   • ទុកឱ្យបុគ្គលិកជំនាញដំណើរការអាជីវកម្មប្រចាំថ្ងៃដោយសេរីភាពពេញលេញ ខណៈពេលដែល CEO ប្រមូលផ្តុំតែលើការសម្រេចចិត្តបែងចែកទុនដ៏មានប្រសិទ្ធភាពបំផុត។"
        ),
        "formula": "Value Per Share Growth = Free Cash Flow Growth / Total Shares Outstanding (Decreasing)",
        "quiz": {
            "question": "តើនៅពេលណាដែលការទិញភាគហ៊ុនខ្លួនឯងមកវិញ (Share Buyback) បង្កើតតម្លៃពិតប្រាកដសម្រាប់ម្ចាស់ភាគហ៊ុន?",
            "options": [
                "A) នៅពេលដែលតម្លៃភាគហ៊ុនលើទីផ្សារ ធ្លាក់ចុះទាបជាងតម្លៃពិតខាងក្នុង (Intrinsic Value)",
                "B) នៅពេលដែលតម្លៃភាគហ៊ុនឡើងដល់កម្រិតខ្ពស់បំផុតដើម្បីអួតទីផ្សារ",
                "C) នៅពេលក្រុមហ៊ុនត្រូវបង្ខំចិត្តខ្ចីបំណុលការប្រាក់ខ្ពស់មកទិញ"
            ],
            "correct_index": 0,
            "explanation": "Share Buybacks បង្កើតតម្លៃមហាសាលបាន លុះត្រាតែទិញនៅពេលតម្លៃទាបជាងតម្លៃពិត (Discount to Intrinsic Value)។ បើទិញពេលថ្លៃហួសហេតុ វានឹងបំផ្លាញតម្លៃរបស់ម្ចាស់ភាគហ៊ុនទៅវិញ!"
        }
    },
    11: {
        "id": 11,
        "tier": "tier_4",
        "book_title": "The Warren Buffett Way",
        "author": "Robert G. Hagstrom",
        "year": 1994,
        "title_km": "មេរៀនទី ១១៖ វិធានមាសទាំង ១២ នៃការវិនិយោគបែប Warren Buffett",
        "title_en": "Lesson 11: The 12 Tenets of the Warren Buffett Way",
        "core_thesis": "ការវិនិយោគជោគជ័យ គឺទាមទារនូវគោលការណ៍ដែលមិនប្រែប្រួលតាមពេលវេលា។",
        "fiduciary_pillar": "Business, Management, Financial & Value Tenets Synthesized",
        "content_km": (
            "📖 សៀវភៅគោល៖ The Warren Buffett Way ដោយ Robert G. Hagstrom\n\n"
            "វិធានមាសទាំង ១២ ត្រូវបានបែងចែកជា ៤ សសរស្តម្ភធំៗ៖\n\n"
            "១. សសរស្តម្ភអាជីវកម្ម (Business Tenets):\n"
            "   • តើអាជីវកម្មនេះសាមញ្ញ និងងាយយល់ដែរឬទេ? (Simple & Understandable)\n"
            "   • តើអាជីវកម្មនេះមានប្រវត្តិដំណើរការជាប់លាប់ដែរឬទេ? (Consistent Operating History)\n"
            "   • តើអាជីវកម្មនេះមានអនាគតវែងឆ្ងាយដែរឬទេ? (Favorable Long-Term Prospects)\n\n"
            "២. សសរស្តម្ភថ្នាក់ដឹកនាំ (Management Tenets):\n"
            "   • តើថ្នាក់ដឹកនាំមានហេតុផលត្រឹមត្រូវដែរឬទេ? (Rational Capital Allocation)\n"
            "   • តើថ្នាក់ដឹកនាំមានភាពស្មោះត្រង់ចំពោះម្ចាស់ភាគហ៊ុនដែរឬទេ? (Candor & Honesty)\n"
            "   • តើថ្នាក់ដឹកនាំអាចទប់ទល់នឹងឥទ្ធិពលចម្លងគ្នាបានដែរឬទេ? (Resist Institutional Imperative)\n\n"
            "៣. សសរស្តម្ភហិរញ្ញវត្ថុ (Financial Tenets):\n"
            "   • ផ្តោតលើផលត្រឡប់លើមូលធន (ROE) មិនមែនត្រឹមតែ EPS នោះទេ។\n"
            "   • គណនាប្រាក់ចំណូលម្ចាស់ (Owner Earnings) ឱ្យបានច្បាស់លាស់។\n"
            "   • ស្វែងរកក្រុមហ៊ុនដែលមានប្រាក់ចំណេញដុលខ្ពស់ (High Profit Margins)។\n"
            "   • វិធាន $1 Premise៖ រាល់ $1 នៃប្រាក់ចំណេញដែលក្រុមហ៊ុនរក្សាទុក ត្រូវបង្កើតបានតម្លៃទីផ្សារយ៉ាងហោចណាស់ $1 ត្រឡប់មកវិញ។\n\n"
            "៤. សសរស្តម្ភតម្លៃ (Value Tenets):\n"
            "   • គណនាតម្លៃពិត (Intrinsic Value) តាមរយៈការបញ្ចុះតម្លៃលំហូរសាច់ប្រាក់ (DCF)។\n"
            "   • ទិញតែនៅពេលដែលមានគម្លាតសុវត្ថិភាព (Margin of Safety >= 25-30%) ប៉ុណ្ណោះ!"
        ),
        "formula": "$1 Retained Value Test: Change in Market Cap >= Retained Earnings over 5 Years",
        "quiz": {
            "question": "តើ 'វិធាន $1 Premise' របស់ Warren Buffett មានន័យដូចម្តេច?",
            "options": [
                "A) រាល់ $1 ដែលក្រុមហ៊ុនរក្សាទុកមិនចែកភាគលាភ ត្រូវបង្កើតតម្លៃទីផ្សារយ៉ាងតិច $1 ត្រឡប់មកវិញក្នុងរយៈពេលវែង",
                "B) ភាគហ៊ុនទាំងអស់ត្រូវតែមានតម្លៃ $1 ក្នុងមួយហ៊ុន",
                "C) វិនិយោគិនត្រូវចាប់ផ្តើមទិញភាគហ៊ុនដោយប្រាក់ $1 ដំបូង"
            ],
            "correct_index": 0,
            "explanation": "វិធាន $1 Premise ធានាថាថ្នាក់ដឹកនាំមិនយកលុយម្ចាស់ភាគហ៊ុនទៅដេកស៊ី ឬវិនិយោគឥតប្រយោជន៍។ ប្រសិនបើទុក $1 ហើយតម្លៃក្រុមហ៊ុនមិនកើនលើសពី $1 ទេ នោះក្រុមហ៊ុនគួរបង្វែរសាច់ប្រាក់នោះចែកជាភាគលាភវិញ!"
        }
    },
    12: {
        "id": 12,
        "tier": "tier_4",
        "book_title": "Buffett: The Making of an American Capitalist & Angkor Quant Synthesis",
        "author": "Roger Lowenstein & Angkor Quant AI Team",
        "year": 1995,
        "title_km": "មេរៀនទី ១២៖ សំយោគស្ថាបត្យកម្មវិនិយោគបរិមាណ (Angkor Quant Algorithmic Value)",
        "title_en": "Lesson 12: Quantitative Value Synthesis & Autonomous Compounding",
        "core_thesis": "ការវិនិយោគដោយគ្មានគំរូគណិតវិទ្យា និងវិន័យស្វ័យប្រវត្តិនឹងត្រូវចាញ់បោកអារម្មណ៍មនុស្ស។ វិស្វកម្មបរិមាណការពារមូលធន ១០០%។",
        "fiduciary_pillar": "DCF Modeling, Fractional Kelly Parity & Zero Technical Negligence (AQ69)",
        "content_km": (
            "📖 សៀវភៅគោល៖ Buffett ដោយ Roger Lowenstein + សំយោគប្រព័ន្ធ ANGKOR QUANT\n\n"
            "១. ការរួមបញ្ចូលគ្នារវាង 'គុណភាព Buffett' និង 'គណិតវិទ្យាបរិមាណ Quant':\n"
            "   • អារម្មណ៍របស់មនុស្សងាយនឹងចុះចាញ់ភាពភ័យខ្លាច និងការលោភលន់។ ដូច្នេះ Angkor Quant បានបំប្លែងទស្សនវិជ្ជារបស់ Buffett ទៅជាក្បួនដោះស្រាយគណិតវិទ្យាជាក់ស្តែង៖\n"
            "     - Owner Earnings & DCF Algorithmic Engine: គណនាតម្លៃពិតស្វ័យប្រវត្តិ។\n"
            "     - Piotroski F-Score (9/9 Points): ត្រួតពិនិត្យសុខភាពហិរញ្ញវត្ថុ ៩ ចំណុចដោយមិនលម្អៀង។\n"
            "     - Altman Z-Score: កម្ចាត់ចោលក្រុមហ៊ុនប្រឈមនឹងការក្ស័យធន (Z < 1.81)។\n"
            "     - Fractional Kelly Criterion: បែងចែកទំហំទុនតាមគណិតវិទ្យា មិនឱ្យមានហានិភ័យ Gambler's Ruin ឡើយ។\n\n"
            "២. វិធាន ២ យ៉ាងដែលមិនអាចកែប្រែបានរបស់ Warren Buffett:\n"
            "   • Rule #1: កុំឱ្យខាតបង់ដើមទុនជាដាច់ខាត (Never Lose Capital)!\n"
            "   • Rule #2: កុំភ្លេចវិធានទី ១ ជាដាច់ខាត (Never Forget Rule #1)!\n\n"
            "៣. ស្បថសច្ចា Fiduciary Oath របស់ Angkor Quant:\n"
            "   • យើងប្រើប្រាស់បច្ចេកវិទ្យា Python, Electron.js, Telegram Bot និង Telegram Mini App ដើម្បីដឹកនាំប្រជាជនកម្ពុជាឱ្យចាកចេញពីល្បែងភ្នាល់ Zero-Sum Gamble ហើយឈានចូលក្នុងមាគ៌ាវិនិយោគិនពិតប្រាកដដែលកសាងទ្រព្យសម្បត្តិយូរអង្វែងតកូនតចៅ!"
        ),
        "formula": "Intrinsic Value DCF = Sum(CF_t / (1 + r)^t) + Terminal_Value / (1 + r)^n",
        "quiz": {
            "question": "តើវិធានទី ១ និងវិធានទី ២ ដ៏ល្បីល្បាញបំផុតរបស់ Warren Buffett គឺជាអ្វី?",
            "options": [
                "A) វិធានទី ១៖ ព្យាយាមរកចំណេញឱ្យបានលឿនបំផុត | វិធានទី ២៖ ប្រើ Leverage ឱ្យអស់ពីសមត្ថភាព",
                "B) វិធានទី ១៖ ដាច់ខាតកុំឱ្យខាតបង់ដើមទុន | វិធានទី ២៖ ដាច់ខាតកុំភ្លេចវិធានទី ១",
                "C) វិធានទី ១៖ ទិញតាមអារម្មណ៍ | វិធានទី ២៖ លក់នៅពេលភ័យខ្លាច"
            ],
            "correct_index": 1,
            "explanation": "Rule #1: Never lose money. Rule #2: Never forget Rule #1. នេះគឺជាបេះដូងនៃ Angkor Quant Fiduciary Engine ដើម្បីធានាថាដើមទុនត្រូវបានការពារជានិច្ច!"
        }
    }
}

# ==============================================================================
# QUANTITATIVE MATHEMATICAL VALUATION & RISK ENGINES
# ==============================================================================

class BuffettValuationEngine:
    """
    Mathematical Implementation of Warren Buffett's Valuation Models:
    1. Owner Earnings Model (1986 Shareholder Letter)
    2. 2-Stage Discounted Cash Flow (DCF) with Terminal Value
    3. Piotroski F-Score Fundamental Quality Matrix (0 to 9 points)
    4. Altman Z-Score Bankruptcy Distress Model
    5. Fractional Kelly Criterion for Risk Parity Sizing
    6. Snowball Exponential Compounding Wealth Simulator
    """

    @staticmethod
    def calculate_owner_earnings(
        net_income: float,
        depreciation_amortization: float,
        maintenance_capex: float,
        working_capital_change: float = 0.0
    ) -> Dict[str, Any]:
        """
        Owner Earnings = Net Income + D&A - Maintenance CapEx +/- Delta Working Capital
        Returns detailed breakdown and per-share metric.
        """
        owner_earnings = (
            net_income + depreciation_amortization - maintenance_capex + working_capital_change
        )
        ratio_to_net_income = (owner_earnings / net_income) if net_income > 0 else 0.0
        
        quality = "HIGH_QUALITY" if ratio_to_net_income >= 1.0 else "CAPEX_HEAVY"
        return {
            "owner_earnings": round(owner_earnings, 2),
            "net_income": round(net_income, 2),
            "depreciation_amortization": round(depreciation_amortization, 2),
            "maintenance_capex": round(maintenance_capex, 2),
            "working_capital_change": round(working_capital_change, 2),
            "ratio_to_net_income": round(ratio_to_net_income, 2),
            "quality": quality,
            "formula_repr": f"${net_income:,.1f} + ${depreciation_amortization:,.1f} - ${maintenance_capex:,.1f} = ${owner_earnings:,.1f}"
        }

    @staticmethod
    def calculate_dcf_intrinsic_value(
        current_fcf: float,
        growth_rate_5y: float = 0.08,
        terminal_growth: float = 0.025,
        discount_rate: float = 0.09,
        shares_outstanding: float = 1.0,
        current_cash: float = 0.0,
        total_debt: float = 0.0,
        margin_of_safety_pct: float = 0.30
    ) -> Dict[str, Any]:
        """
        Calculates 2-Stage DCF Intrinsic Value:
        - Stage 1: 5 Years explicit growth
        - Stage 2: Terminal Value via Gordon Growth Model
        - Enterprise Value -> Equity Value (adding net cash)
        - Per-Share Intrinsic Value & Margin of Safety Target Price
        """
        if discount_rate <= terminal_growth:
            discount_rate = terminal_growth + 0.01

        projected_cash_flows = []
        discounted_cash_flows = []
        cf = current_fcf

        for yr in range(1, 6):
            cf = cf * (1.0 + growth_rate_5y)
            discount_factor = 1.0 / ((1.0 + discount_rate) ** yr)
            d_cf = cf * discount_factor
            projected_cash_flows.append(round(cf, 2))
            discounted_cash_flows.append(round(d_cf, 2))

        # Terminal Value at Year 5
        terminal_cf = cf * (1.0 + terminal_growth)
        terminal_value = terminal_cf / (discount_rate - terminal_growth)
        discounted_terminal_value = terminal_value / ((1.0 + discount_rate) ** 5)

        pv_operating = sum(discounted_cash_flows) + discounted_terminal_value
        equity_value = pv_operating + current_cash - total_debt
        intrinsic_per_share = (equity_value / shares_outstanding) if shares_outstanding > 0 else 0.0
        buy_below_price = intrinsic_per_share * (1.0 - margin_of_safety_pct)

        return {
            "current_fcf": current_fcf,
            "projected_fcf_5y": projected_cash_flows,
            "discounted_fcf_5y": discounted_cash_flows,
            "terminal_value": round(terminal_value, 2),
            "discounted_terminal_value": round(discounted_terminal_value, 2),
            "enterprise_value": round(pv_operating, 2),
            "equity_value": round(equity_value, 2),
            "intrinsic_value_per_share": round(intrinsic_per_share, 2),
            "buy_below_price": round(buy_below_price, 2),
            "margin_of_safety_pct": margin_of_safety_pct,
            "parameters": {
                "growth_5y": f"{growth_rate_5y*100:.1f}%",
                "terminal_growth": f"{terminal_growth*100:.1f}%",
                "discount_rate": f"{discount_rate*100:.1f}%",
                "margin_of_safety": f"{margin_of_safety_pct*100:.1f}%"
            }
        }

    @staticmethod
    def calculate_piotroski_f_score(data: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates 9-Point Piotroski Fundamental F-Score:
        Profitability:
        1. ROA > 0 (1 pt)
        2. CFO > 0 (1 pt)
        3. Delta ROA > 0 (1 pt)
        4. Accrual: CFO > ROA (1 pt)
        Leverage & Liquidity:
        5. Delta Long-term Debt <= 0 (1 pt)
        6. Delta Current Ratio > 0 (1 pt)
        7. Zero Share Dilution (1 pt)
        Operating Efficiency:
        8. Delta Gross Margin > 0 (1 pt)
        9. Delta Asset Turnover > 0 (1 pt)
        """
        score = 0
        breakdown = {}

        # 1. ROA > 0
        roa_pos = data.get("net_income", 0) > 0
        score += 1 if roa_pos else 0
        breakdown["roa_positive"] = roa_pos

        # 2. CFO > 0
        cfo_pos = data.get("cfo", 0) > 0
        score += 1 if cfo_pos else 0
        breakdown["cfo_positive"] = cfo_pos

        # 3. Delta ROA > 0
        delta_roa = data.get("roa_current", 0) > data.get("roa_prior", 0)
        score += 1 if delta_roa else 0
        breakdown["delta_roa_positive"] = delta_roa

        # 4. CFO > Net Income (Quality of earnings)
        quality = data.get("cfo", 0) > data.get("net_income", 0)
        score += 1 if quality else 0
        breakdown["quality_cfo_gt_ni"] = quality

        # 5. Delta Long Term Debt <= 0
        debt_down = data.get("lt_debt_current", 0) <= data.get("lt_debt_prior", 0)
        score += 1 if debt_down else 0
        breakdown["lt_debt_reduced"] = debt_down

        # 6. Delta Current Ratio > 0
        cr_up = data.get("current_ratio_current", 0) > data.get("current_ratio_prior", 0)
        score += 1 if cr_up else 0
        breakdown["current_ratio_improved"] = cr_up

        # 7. Zero Dilution
        no_dilution = data.get("shares_current", 1) <= data.get("shares_prior", 1)
        score += 1 if no_dilution else 0
        breakdown["no_share_dilution"] = no_dilution

        # 8. Delta Gross Margin > 0
        gm_up = data.get("gross_margin_current", 0) >= data.get("gross_margin_prior", 0)
        score += 1 if gm_up else 0
        breakdown["gross_margin_expanded"] = gm_up

        # 9. Delta Asset Turnover > 0
        at_up = data.get("asset_turnover_current", 0) >= data.get("asset_turnover_prior", 0)
        score += 1 if at_up else 0
        breakdown["asset_turnover_improved"] = at_up

        rating = "STRONG_MOAT" if score >= 8 else ("SOUND" if score >= 5 else "WEAK_DISTRESS")
        return {
            "f_score": score,
            "max_score": 9,
            "rating": rating,
            "breakdown": breakdown
        }

    @staticmethod
    def calculate_compound_snowball(
        initial_capital: float = 1000.0,
        monthly_addition: float = 100.0,
        annual_roi_pct: float = 15.0,
        years: int = 20
    ) -> Dict[str, Any]:
        """
        Simulates Snowball Wealth Compounding:
        Shows growth trajectory across years comparing:
        1. Disciplined Compounding with No Ruin
        2. Linear Cash Savings with 0% ROI
        3. Reckless Gambler Path (Drawdown / Wipeout)
        """
        r_monthly = (annual_roi_pct / 100.0) / 12.0
        trajectory = []
        compounded_bal = initial_capital
        linear_savings = initial_capital

        for y in range(1, years + 1):
            for _ in range(12):
                compounded_bal = (compounded_bal + monthly_addition) * (1.0 + r_monthly)
                linear_savings += monthly_addition
            
            # Theoretical gambler path with -30% ruin probability
            gambler_bal = round(initial_capital * ((1.0 - 0.25) ** (y * 0.5)), 2) if y >= 2 else round(initial_capital * 1.2, 2)
            
            trajectory.append({
                "year": y,
                "compounded_balance": round(compounded_bal, 2),
                "linear_savings": round(linear_savings, 2),
                "wealth_multiplier": round(compounded_bal / linear_savings, 2),
                "gambler_balance": gambler_bal
            })

        total_contributions = initial_capital + (monthly_addition * 12 * years)
        compound_profit = round(compounded_bal - total_contributions, 2)

        return {
            "initial_capital": initial_capital,
            "monthly_addition": monthly_addition,
            "annual_roi_pct": annual_roi_pct,
            "years": years,
            "final_compounded_balance": round(compounded_bal, 2),
            "total_contributions": round(total_contributions, 2),
            "compound_profit": compound_profit,
            "trajectory": trajectory
        }

    @staticmethod
    def calculate_fractional_kelly(
        win_rate: float = 0.60,
        win_loss_ratio: float = 2.5,
        fraction: float = 0.25
    ) -> Dict[str, Any]:
        """
        Fractional Kelly Criterion:
        f* = (p*(b+1) - 1) / b
        fractional_f = f* * fraction (Quarter Kelly recommended for institutional zero-ruin)
        """
        p = win_rate
        q = 1.0 - p
        b = win_loss_ratio

        full_kelly = (p * (b + 1.0) - 1.0) / b
        full_kelly = max(0.0, full_kelly)
        fractional_kelly = full_kelly * fraction

        # Clamp between 0.5% and 5.0% for institutional capital preservation
        safe_allocation_pct = min(max(fractional_kelly * 100.0, 0.5), 5.0)

        return {
            "win_rate": round(win_rate * 100, 1),
            "risk_reward_ratio": f"1:{win_loss_ratio:.1f}",
            "full_kelly_pct": round(full_kelly * 100, 2),
            "fractional_kelly_pct": round(safe_allocation_pct, 2),
            "recommendation_km": f"បែងចែកទំហំទុនអតិបរមា {safe_allocation_pct:.1f}% នៃកាបូប ដើម្បីលុបបំបាត់ហានិភ័យក្ស័យធន ១០០%!"
        }

# ==============================================================================
# FIDUCIARY GRADUATE CERTIFICATE GENERATOR & SHA-256 VERIFIER
# ==============================================================================

class FiduciaryCertificateManager:
    """
    Issues and cryptographically verifies Angkor Quant Fiduciary Academy Certificates.
    Prevents forged or modified credentials through SHA-256 HMAC digital signatures.
    """
    SECRET_SALT = "ANGKOR_QUANT_FIDUCIARY_INTEGRITY_SALT_2026_AQ69"

    @classmethod
    def generate_certificate(
        cls,
        user_id: int,
        user_name: str,
        rank: str = "BLACK_BELT",
        score_pct: float = 100.0
    ) -> Dict[str, Any]:
        """
        Generates a verified graduate record with unique serial number and SHA-256 signature.
        """
        timestamp = int(time.time())
        date_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(timestamp))
        serial_number = f"AQ-BUFFETT-{user_id % 100000:05d}-{timestamp % 100000:05d}"

        payload = f"{user_id}:{user_name}:{rank}:{serial_number}:{timestamp}:{cls.SECRET_SALT}"
        cert_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        rank_titles = {
            "WHITE_BELT": ("🥋 សខ្សែក្រវាត់ស", "White Belt - Disciplined Observer"),
            "GREEN_BELT": ("🥋 ខ្សែក្រវាត់បៃតង", "Green Belt - Financial Forensics Analyst"),
            "BROWN_BELT": ("🥋 ខ្សែក្រវាត់ត្នោត", "Brown Belt - Capital Allocator"),
            "BLACK_BELT": ("🥋 ខ្សែក្រវាត់ខ្មៅ", "Black Belt - Quantitative Fiduciary Master")
        }
        rank_km, rank_en = rank_titles.get(rank, ("🎓 បរិញ្ញាបត្រវិនិយោគ", "Quant Graduate"))

        return {
            "serial_number": serial_number,
            "user_id": user_id,
            "user_name": user_name,
            "rank": rank,
            "rank_km": rank_km,
            "rank_en": rank_en,
            "score_pct": score_pct,
            "issued_at": date_str,
            "timestamp": timestamp,
            "cert_hash": cert_hash,
            "verification_code": cert_hash[:16].upper()
        }

    @classmethod
    def verify_certificate(
        cls,
        user_id: int,
        user_name: str,
        rank: str,
        serial_number: str,
        timestamp: int,
        cert_hash: str
    ) -> bool:
        """
        Validates the authenticity of an Angkor Quant certificate.
        """
        payload = f"{user_id}:{user_name}:{rank}:{serial_number}:{timestamp}:{cls.SECRET_SALT}"
        expected_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return expected_hash == cert_hash

# Global Singleton Engine Instance
_academy_engine = None

def get_academy_engine():
    global _academy_engine
    if _academy_engine is None:
        _academy_engine = BuffettValuationEngine()
    return _academy_engine


# ==============================================================================
# TELEGRAM BOT INTERACTIVE UI BUILDERS & TELEMETRY SUITE
# ==============================================================================

def build_academy_home_payload(chat_id: int, user_lang: str = "km") -> Tuple[str, Any]:
    """Generates the main Angkor Quant Fiduciary Academy Telemetry dashboard."""
    import database as db
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    progress = db.get_academy_user_progress(chat_id)
    rank = progress.get("rank", "WHITE_BELT")
    xp = progress.get("xp", 0)
    completed_lessons = progress.get("completed_lessons", [])
    quizzes_passed = progress.get("quizzes_passed", [])
    next_lesson = progress.get("next_lesson", 1)

    rank_titles = {
        "WHITE_BELT": ("🥋 សខ្សែក្រវាត់ស", "White Belt - Disciplined Observer"),
        "GREEN_BELT": ("🥋 ខ្សែក្រវាត់បៃតង", "Green Belt - Financial Forensics Analyst"),
        "BROWN_BELT": ("🥋 ខ្សែក្រវាត់ត្នោត", "Brown Belt - Capital Allocator"),
        "BLACK_BELT": ("🥋 ខ្សែក្រវាត់ខ្មៅ", "Black Belt - Quantitative Fiduciary Master")
    }
    badge_km, badge_en = rank_titles.get(rank, ("🎓 សិស្សវិនិយោគ", "Quant Student"))

    msg = (
        f"🎓 *ANGKOR QUANT FIDUCIARY ACADEMY*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🏛️ *សាលាវិនិយោគបរិមាណ & គម្ពីរ Warren Buffett ទាំង ១២*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"👤 *ឋានៈកិត្តិយស:* `{badge_km}`\n"
        f"⭐ *ពិន្ទុវិជ្ជាជីវៈ:* `{xp} XP`\n"
        f"📚 *មេរៀនបានបញ្ចប់:* `{len(completed_lessons)}/12` (មេរៀនបន្ត៖ #{next_lesson})\n"
        f"🎯 *តេស្តបានប្រឡងជាប់:* `{len(quizzes_passed)}/12`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🛡️ *សច្ចាប្រណិធាន FIDUCIARY REFUSAL:*\n"
        f"• *Rule #1:* ដាច់ខាតកុំឱ្យខាតបង់ដើមទុន (Never Lose Capital)!\n"
        f"• *Rule #2:* ដាច់ខាតកុំភ្លេច Rule #1!\n"
        f"• បដិសេធល្បែងស៊ីសង ១០០% | គ្មាន No-SL | គ្មាន Martingale\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"👇 សូមជ្រើសរើសថ្នាក់សិក្សា ឬឧបករណ៍គណនាខាងក្រោម៖\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"_Khmer Master Crypto_\n"
        f"_APEX SUPER BRAIN AI_\n"
        f"មាគ៌ាវិនិយោគិនពិតប្រាកដសម្រាប់ប្រជាជនកម្ពុជា!"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🥋 ថ្នាក់ទី ១ (មេរៀន ១-៣) | Tier 1", callback_data="acad_tier_tier_1"),
            InlineKeyboardButton("🥋 ថ្នាក់ទី ២ (មេរៀន ៤-៦) | Tier 2", callback_data="acad_tier_tier_2")
        ],
        [
            InlineKeyboardButton("🥋 ថ្នាក់ទី ៣ (មេរៀន ៧-១០) | Tier 3", callback_data="acad_tier_tier_3"),
            InlineKeyboardButton("🥋 ថ្នាក់ទី ៤ (មេរៀន ១១-១២) | Tier 4", callback_data="acad_tier_tier_4")
        ],
        [
            InlineKeyboardButton("🧮 គណនា DCF | DCF Lab", callback_data="acad_tool_dcf"),
            InlineKeyboardButton("❄️ ដុំព្រិល Snowball", callback_data="acad_tool_snowball")
        ],
        [
            InlineKeyboardButton("📐 Kelly Risk Sizing", callback_data="acad_tool_kelly"),
            InlineKeyboardButton("📜 សញ្ញាបត្រ Fiduciary", callback_data="acad_certificate")
        ],
        [
            InlineKeyboardButton("🔄 ផ្ទុកឡើងវិញ | Refresh", callback_data="acad_home")
        ]
    ])
    return msg, keyboard

def build_academy_tier_payload(tier_key: str, chat_id: int, user_lang: str = "km") -> Tuple[str, Any]:
    """Generates the view for a specific Tier in the curriculum."""
    import database as db
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    tier_info = ACADEMY_TIERS.get(tier_key, ACADEMY_TIERS["tier_1"])
    progress = db.get_academy_user_progress(chat_id)
    completed_lessons = progress.get("completed_lessons", [])
    quizzes_passed = progress.get("quizzes_passed", [])

    tier_lessons = tier_info["lessons"]

    msg = (
        f"🏛️ *{tier_info['name_km']}*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🎖️ *Badge:* `{tier_info['badge']}`\n"
        f"📖 *គោលបំណង:* {tier_info['desc_km']}\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"📚 *បញ្ជីមេរៀនក្នុងថ្នាក់នេះ:*\n"
    )

    lesson_buttons = []
    for lid in tier_lessons:
        les = ACADEMY_LESSONS[lid]
        done_check = "✅" if lid in completed_lessons else "⏳"
        quiz_check = "🎯" if lid in quizzes_passed else ""
        msg += f"• {done_check} *#{lid}:* {les['book_title']} ({les['author']}) {quiz_check}\n"
        lesson_buttons.append([
            InlineKeyboardButton(
                f"{done_check} មេរៀន #{lid}: {les['book_title'][:22]}",
                callback_data=f"acad_lesson_{lid}"
            )
        ])

    msg += (
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"👇 ចុចលើមេរៀននីមួយៗដើម្បីចាប់ផ្តើមអាន និងធ្វើតេស្ត!"
    )

    lesson_buttons.append([
        InlineKeyboardButton("🔙 ត្រឡប់ទៅទំព័រដើម | Home", callback_data="acad_home")
    ])
    return msg, InlineKeyboardMarkup(lesson_buttons)

def build_academy_lesson_payload(lesson_id: int, chat_id: int, user_lang: str = "km") -> Tuple[str, Any]:
    """Renders full lesson content and records completion XP."""
    import database as db
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    lesson = ACADEMY_LESSONS.get(lesson_id, ACADEMY_LESSONS[1])
    db.record_academy_lesson_completed(chat_id, lesson_id, xp_gain=50)

    progress = db.get_academy_user_progress(chat_id)
    is_quiz_passed = lesson_id in progress.get("quizzes_passed", [])
    quiz_badge = "✅ បានប្រឡងជាប់" if is_quiz_passed else "⏳ មិនទាន់ធ្វើតេស្ត"

    msg = (
        f"🏛️ *ANGKOR QUANT FIDUCIARY ACADEMY*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"📖 *{lesson['title_km']}*\n"
        f"👤 *អ្នកនិពន្ធ:* {lesson['author']} ({lesson['year']})\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"💡 *ទ្រឹស្តីគ្រឹះ:* _{lesson['core_thesis']}_\n"
        f"🛡️ *សសរស្តម្ភ:* `{lesson['fiduciary_pillar']}`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"{lesson['content_km']}\n\n"
        f"📐 *រូបមន្តបរិមាណ Quant:*\n"
        f"`{lesson['formula']}`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🎯 *ស្ថានភាពតេស្ត:* `{quiz_badge}` (+100 XP)\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"_Angkor Quant - Fiduciary Integrity Lock_"
    )

    tier_key = lesson["tier"]
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"❓ ធ្វើតេស្ត Quiz #{lesson_id} (+100 XP)", callback_data=f"acad_quiz_{lesson_id}")
        ],
        [
            InlineKeyboardButton("🔙 ត្រឡប់ទៅថ្នាក់រៀន", callback_data=f"acad_tier_{tier_key}"),
            InlineKeyboardButton("🏠 ទំព័រដើម", callback_data="acad_home")
        ]
    ])
    return msg, keyboard

def build_academy_quiz_payload(lesson_id: int, chat_id: int, user_lang: str = "km") -> Tuple[str, Any]:
    """Generates the interactive multi-choice quiz for a lesson."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    lesson = ACADEMY_LESSONS.get(lesson_id, ACADEMY_LESSONS[1])
    quiz = lesson["quiz"]

    msg = (
        f"🎯 *តេស្តសមត្ថភាព FIDUCIARY QUIZ #{lesson_id}*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"📖 *មេរៀន:* {lesson['book_title']} ({lesson['author']})\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"❓ *សំណួរ:*\n"
        f"_{quiz['question']}_\n\n"
        f"ជម្រើសចម្លើយ:\n"
    )

    buttons = []
    for idx, opt in enumerate(quiz["options"]):
        msg += f"{opt}\n"
        letter = chr(ord('A') + idx)
        buttons.append(InlineKeyboardButton(f"🔘 {letter}", callback_data=f"acad_ans_{lesson_id}_{idx}"))

    msg += (
        f"\n{ui_standards.DIVIDER_HEAVY}\n"
        f"💡 ចុចប៊ូតុងខាងក្រោមដើម្បីជ្រើសរើសចម្លើយត្រឹមត្រូវ (+100 XP)!"
    )

    keyboard = InlineKeyboardMarkup([
        buttons,
        [InlineKeyboardButton("🔙 ត្រឡប់ទៅអានមេរៀន", callback_data=f"acad_lesson_{lesson_id}")]
    ])
    return msg, keyboard

def build_academy_answer_payload(
    lesson_id: int,
    choice_idx: int,
    chat_id: int,
    user_name: str = "Investor",
    user_lang: str = "km"
) -> Tuple[str, Any]:
    """Evaluates quiz answer, awards XP, and returns feedback."""
    import database as db
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    lesson = ACADEMY_LESSONS.get(lesson_id, ACADEMY_LESSONS[1])
    quiz = lesson["quiz"]
    correct_idx = quiz["correct_index"]

    is_correct = (choice_idx == correct_idx)
    db.record_academy_quiz_result(chat_id, lesson_id, score=1 if is_correct else 0, total=1, passed=is_correct, xp_gain=100)

    progress = db.get_academy_user_progress(chat_id)
    xp = progress.get("xp", 0)
    rank = progress.get("rank", "WHITE_BELT")

    if is_correct:
        msg = (
            f"🎉 *អបអរសាទរ! ចម្លើយរបស់អ្នកត្រឹមត្រូវ ១០០%!* 💎\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"⭐ *រង្វាន់:* `+100 XP` (សរុប: {xp} XP)\n"
            f"🎖️ *ឋានៈបច្ចុប្បន្ន:* `{rank}`\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"💡 *ការពន្យល់បែបវិស្វកម្មបរិមាណ:*\n"
            f"{quiz['explanation']}\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"✨ អ្នកបានយល់ច្បាស់ពីសសរស្តម្ភ {lesson['fiduciary_pillar']}!"
        )
        next_lid = lesson_id + 1 if lesson_id < 12 else 1
        nav_buttons = [
            [InlineKeyboardButton(f"➡️ បន្តទៅមេរៀន #{next_lid}", callback_data=f"acad_lesson_{next_lid}")],
            [InlineKeyboardButton("🏠 ទំព័រដើម Academy", callback_data="acad_home")]
        ]
    else:
        msg = (
            f"⚠️ *ចម្លើយមិនទាន់ត្រឹមត្រូវឡើយ!* 🛡️\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"💡 *ការពន្យល់ណែនាំ:*\n"
            f"{quiz['explanation']}\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"កុំបារម្ភ! វិនិយោគិនពិតប្រាកដរៀនសូត្រពីកំហុស។ ចូរអានមេរៀនឡើងវិញ និងសាកល្បងម្តងទៀត!"
        )
        nav_buttons = [
            [InlineKeyboardButton(f"🔄 សាកល្បងតេស្តឡើងវិញ", callback_data=f"acad_quiz_{lesson_id}")],
            [InlineKeyboardButton(f"📖 អានមេរៀន #{lesson_id}", callback_data=f"acad_lesson_{lesson_id}")]
        ]

    return msg, InlineKeyboardMarkup(nav_buttons)

def build_academy_dcf_tool_payload(chat_id: int, user_lang: str = "km") -> Tuple[str, Any]:
    """Renders a live demonstration of Discounted Cash Flow valuation."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    dcf = BuffettValuationEngine.calculate_dcf_intrinsic_value(
        current_fcf=120.0,
        growth_rate_5y=0.09,
        terminal_growth=0.025,
        discount_rate=0.095,
        shares_outstanding=10.0,
        current_cash=30.0,
        total_debt=10.0,
        margin_of_safety_pct=0.30
    )

    msg = (
        f"🧮 *ANGKOR QUANT DCF VALUATION LAB*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🏛️ *គំរូតម្លៃពិតលំហូរសាច់ប្រាក់បញ្ចុះ (2-Stage DCF)*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"📊 *ប៉ារ៉ាម៉ែត្រអាជីវកម្មគំរូ:*\n"
        f"• Free Cash Flow (FCF): `$120.0M`\n"
        f"• កំណើន ៥ ឆ្នាំដំបូង: `9.0%`\n"
        f"• កំណើន Terminal Growth: `2.5%`\n"
        f"• អត្រាបញ្ចុះតម្លៃ (Discount Rate): `9.5%`\n"
        f"• ចំនួនភាគហ៊ុន: `10.0M ហ៊ុន`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"💎 *លទ្ធផលតម្លៃពិត (Intrinsic Value):*\n"
        f"• តម្លៃសហគ្រាស (Enterprise Value): `${dcf['enterprise_value']:,.1f}M`\n"
        f"• តម្លៃមូលធនម្ចាស់ (Equity Value): `${dcf['equity_value']:,.1f}M`\n"
        f"• *តម្លៃពិតក្នុងមួយហ៊ុន:* `${dcf['intrinsic_value_per_share']:.2f}`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🛡️ *គម្លាតសុវត្ថិភាព (30% Margin of Safety):*\n"
        f"• *តម្លៃគោលដៅទិញ (Buy Below):* `${dcf['buy_below_price']:.2f}`\n"
        f"💡 បើតម្លៃទីផ្សារធ្លាក់ដល់ `${dcf['buy_below_price']:.2f}` ឬទាបជាងនេះ នោះជាឱកាសមាសដែលការពារដើមទុន 100%!"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("❄️ មើលដុំព្រិល Snowball", callback_data="acad_tool_snowball")],
        [InlineKeyboardButton("🔙 ត្រឡប់ទៅទំព័រដើម | Home", callback_data="acad_home")]
    ])
    return msg, keyboard

def build_academy_snowball_tool_payload(chat_id: int, user_lang: str = "km") -> Tuple[str, Any]:
    """Renders a live demonstration of Snowball Exponential Compounding."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    snowball = BuffettValuationEngine.calculate_compound_snowball(
        initial_capital=1000.0,
        monthly_addition=100.0,
        annual_roi_pct=15.0,
        years=20
    )

    msg = (
        f"❄️ *ANGKOR QUANT SNOWBALL COMPOUNDING LAB*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🏔️ *អព្ភូតហេតុទី ៨: ការប្រាក់បង្កើនផលដុំព្រិល*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"💵 *ដើមទុនដំបូង:* `$1,000`\n"
        f"📥 *សន្សំបន្ថែមប្រចាំខែ:* `$100 / ខែ`\n"
        f"📈 *ផលត្រឡប់មធ្យម:* `15.0% / ឆ្នាំ` (កម្រិត Buffett)\n"
        f"⏳ *រយៈពេល:* `20 ឆ្នាំ`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🏆 *លទ្ធផលក្រោយ ២០ ឆ្នាំ:*\n"
        f"• លុយដើមសន្សំបូកបញ្ចូល: `${snowball['total_contributions']:,.0f}`\n"
        f"• *ទ្រព្យសម្បត្តិដុំព្រិលសរុប:* `${snowball['final_compounded_balance']:,.0f}`\n"
        f"• ផលចំណេញពី Compound: `+${snowball['compound_profit']:,.0f}`\n"
        f"• មេគុណបង្កើនផល (Multiplier): `{snowball['final_compounded_balance']/snowball['total_contributions']:.1f}x ដង!`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"📊 *គន្លងប្រៀបធៀបតាមឆ្នាំ:*\n"
    )

    # Show years 5, 10, 15, 20
    for yr in [5, 10, 15, 20]:
        item = snowball["trajectory"][yr - 1]
        msg += f"• ឆ្នាំទី {yr:02d}: `${item['compounded_balance']:,.0f}` (លុយសន្សំធម្មតា: `${item['linear_savings']:,.0f}`)\n"

    msg += (
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"💡 នេះជាមូលហេតុដែលវិនិយោគិនពិត មិនលេងល្បែងប្រថុយដើមទុនឡើយ!"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧮 គណនា DCF Lab", callback_data="acad_tool_dcf")],
        [InlineKeyboardButton("🔙 ត្រឡប់ទៅទំព័រដើម | Home", callback_data="acad_home")]
    ])
    return msg, keyboard

def build_academy_kelly_tool_payload(chat_id: int, user_lang: str = "km") -> Tuple[str, Any]:
    """Renders Fractional Kelly dynamic risk parity calculations."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    kelly = BuffettValuationEngine.calculate_fractional_kelly(
        win_rate=0.60,
        win_loss_ratio=2.5,
        fraction=0.25
    )

    msg = (
        f"📐 *ANGKOR QUANT FRACTIONAL KELLY RISK SIZER*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🏛️ *រូបមន្តគណិតវិទ្យាលុបបំបាត់ Gambler's Ruin ១០០%*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🎯 *ប៉ារ៉ាម៉ែត្រយុទ្ធសាស្ត្រ:*\n"
        f"• អត្រាឈ្នះ (Win Rate): `{kelly['win_rate']}%`\n"
        f"• អនុបាតចំណេញធៀបខាត (R:R): `{kelly['risk_reward_ratio']}`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"⚖️ *លទ្ធផលបែងចែកទំហំទុន:*\n"
        f"• Full Kelly (គ្រោះថ្នាក់): `{kelly['full_kelly_pct']}%`\n"
        f"• *Quarter Kelly (ស្តង់ដារ Angkor Quant):* `{kelly['fractional_kelly_pct']}%`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🛡️ *ការណែនាំវិជ្ជាជីវៈ:*\n"
        f"{kelly['recommendation_km']}\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"កុំដាក់ទុនលើសពី {kelly['fractional_kelly_pct']}% ក្នុងមួយជើងជាដាច់ខាត!"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ត្រឡប់ទៅទំព័រដើម | Home", callback_data="acad_home")]
    ])
    return msg, keyboard

def build_academy_certificate_payload(
    chat_id: int,
    user_name: str = "Valued Investor",
    user_lang: str = "km"
) -> Tuple[str, Any]:
    """Generates and verifies student Fiduciary Certificate."""
    import database as db
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    progress = db.get_academy_user_progress(chat_id)
    completed = progress.get("completed_lessons", [])
    quizzes = progress.get("quizzes_passed", [])
    rank = progress.get("rank", "WHITE_BELT")

    if len(completed) < 3:
        msg = (
            f"📜 *ANGKOR QUANT FIDUCIARY CERTIFICATE*\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"⚠️ *មិនទាន់គ្រប់លក្ខខណ្ឌបញ្ចប់ការសិក្សា!*\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"អ្នកបានបញ្ចប់មេរៀន: `{len(completed)}/12`\n"
            f"អ្នកត្រូវបញ្ចប់យ៉ាងហោចណាស់ ៣ មេរៀនដំបូង (ថ្នាក់ White Belt) ដើម្បីទទួលបានសញ្ញាបត្រកិត្តិយសដំបូង!\n"
            f"{ui_standards.DIVIDER_HEAVY}\n"
            f"👇 ចុចខាងក្រោមដើម្បីបន្តការសិក្សា!"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📖 ទៅថ្នាក់ទី ១ (មេរៀន ១-៣)", callback_data="acad_tier_tier_1")],
            [InlineKeyboardButton("🏠 ទំព័រដើម Academy", callback_data="acad_home")]
        ])
        return msg, keyboard

    cert = FiduciaryCertificateManager.generate_certificate(
        user_id=chat_id,
        user_name=user_name,
        rank=rank,
        score_pct=round((len(quizzes) / max(1, len(completed))) * 100, 1)
    )
    db.save_academy_certificate(cert)

    msg = (
        f"📜 *សញ្ញាបត្រវិនិយោគិនកិត្តិយស ANGKOR QUANT*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🏛️ *ANGKOR QUANT FIDUCIARY GRADUATE DIPLOMA*\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"👤 *ម្ចាស់សញ្ញាបត្រ:* `{user_name}` (ID: `{chat_id}`)\n"
        f"🎖️ *កម្រិតខ្សែក្រវាត់:* `{cert['rank_km']}`\n"
        f"⭐ *ចំណងជើង:* `{cert['rank_en']}`\n"
        f"🎯 *លទ្ធផលតេស្ត:* `{cert['score_pct']}%`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🔑 *លេខកូដសញ្ញាបត្រ:* `{cert['serial_number']}`\n"
        f"🔒 *SHA-256 Hash:* `{cert['verification_code']}`\n"
        f"📅 *កាលបរិច្ឆេទចេញ:* `{cert['issued_at']}`\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"🛡️ *សច្ចាប្រណិធានស្មោះត្រង់វិស្វកម្ម:*\n"
        f"បានបញ្ចប់វគ្គបណ្តុះបណ្តាលគម្ពីរវិនិយោគទាំង ១២ របស់ Warren Buffett និងបានស្បថសច្ចាការពារមូលធន មិនលេងល្បែងភ្នាល់ និងប្រកាន់ខ្ជាប់នូវ Fiduciary Duty ២៤/៧!\n"
        f"{ui_standards.DIVIDER_HEAVY}\n"
        f"_Angkor Quant - Autonomous Quantitative Intelligence_"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 ត្រឡប់ទៅទំព័រដើម Academy", callback_data="acad_home")]
    ])
    return msg, keyboard

