from fastapi import APIRouter

router = APIRouter(prefix="/info", tags=["info"])

REFERRAL_RULES = [
    "Eligibility:\n"
    "  • All existing Carton Caps users with a verified account are eligible to refer friends.\n"
    "  • Referred users must be new to the Carton Caps program.\n"
    "  • Each user must be a legal resident of the United States.",

    "Referral Process:\n"
    "  • Users can share a unique referral code or link via the Carton Caps app.\n"
    "  • The referred user must use the referral code or link during the sign-up process or within a defined window after first installing the app (e.g., within 48 hours).",

    "Reward Structure:\n"
    "  • Referrer Bonus: The referrer receives a bonus (e.g., $5 or equivalent in Carton Caps credits) when:\n"
    "    1. The referred user completes onboarding, and\n"
    "    2. Performs a qualifying action (e.g., makes their first eligible product scan or links to a school).\n"
    "  • Referred User Bonus: The new user receives a welcome bonus (e.g., $5) upon successful sign-up and qualifying action.\n"
    "  • Bonuses are credited to Carton Caps accounts and may be limited to school donations.",

    "Limitations & Abuse:\n"
    "  • Self-referrals are not allowed (e.g., same device, email, or payment method).\n"
    "  • Carton Caps may use fraud detection to block suspicious referrals or accounts.\n"
    "  • Referrals may not be paid for or promoted via misleading methods (spam, bots, etc.).",

    "Program Changes:\n"
    "  • Carton Caps reserves the right to:\n"
    "    1. Modify or terminate the referral program at any time.\n"
    "    2. Withhold rewards for suspected abuse."
]


REFERRAL_FAQS = [
    {
        "id": 1,
        "question": "What is the Carton Caps Referral Program?",
        "answer": (
            "The Carton Caps Referral Program allows you to invite your friends to join the Carton Caps app. "
            "When your friend signs up using your unique referral link and completes onboarding, both of "
            "you receive a special bonus in your Carton Caps accounts."
        )
    },
    {
        "id": 2,
        "question": "How do I refer a friend?",
        "answer": (
            "You can refer a friend directly from the Carton Caps app. Simply:\n"
            "• Tap on the account icon to see account options.\n"
            "• Tap “Invite Friends” from the menu.\n"
            "• Copy the referral code and send to your friend –or– share a link by using the buttons in "
            "the “Share Now” section.\n"
            "• Your friend must install the app using your link or sign up using your code."
        )
    },
    {
        "id": 3,
        "question": "What does my friend experience when they join via my link?",
        "answer": (
            "Referred users get a customized onboarding experience that introduces them to Carton Caps "
            "and highlights how the program supports schools. They'll also be notified about the bonus "
            "they and you will receive."
        )
    },
    {
        "id": 4,
        "question": "When do we receive the bonus?",
        "answer": (
            "Both you and your referred friend will receive the bonus after your friend completes onboarding "
            "and links their Carton Caps account to a preferred school to support."
        )
    },
    {
        "id": 5,
        "question": "What kind of bonus do we get?",
        "answer": (
            "The bonus may vary from time to time. It could be additional Carton Caps points or a special "
            "in-app reward. The current bonus will be displayed on the referral page in the app."
        )
    },
    {
        "id": 6,
        "question": "Can I refer more than one person?",
        "answer": (
            "Absolutely! There's no limit to how many friends you can invite. You’ll earn a bonus for each "
            "successful referral!"
        )
    },
    {
        "id": 7,
        "question": "My friend forgot to use my link. Can we still get the bonus?",
        "answer": (
            "Unfortunately, referrals must be tracked through your unique link. If your friend signs up without "
            "it, the referral won’t be credited automatically."
        )
    },
    {
        "id": 8,
        "question": "Can I refer someone who already uses Carton Caps?",
        "answer": (
            "The referral program is only available for new users. Existing users or users who uninstall and "
            "reinstall the app are not eligible for referral bonuses."
        )
    },
    {
        "id": 9,
        "question": "How can I track my referrals?",
        "answer": (
            "In the “Refer a Friend” section of the app, you can view the status of each referral – whether "
            "your friend has signed up, completed onboarding, and whether your bonus has been awarded."
        )
    },
    {
        "id": 10,
        "question": "Why haven’t I received my bonus yet?",
        "answer": (
            "There may be a delay if your referred friend hasn’t completed onboarding or hasn’t linked to a school. "
            "If it’s been more than 48 hours and you believe there's an issue, contact our support team via the app."
        )
    },
    {
        "id": 11,
        "question": "Are there any restrictions or abuse policies?",
        "answer": (
            "Yes. Carton Caps reserves the right to withhold bonuses or disable accounts if we detect fraudulent "
            "or abusive behavior, including self-referrals, spamming, or fake accounts."
        )
    }
]

@router.get("/faqs")
async def get_faqs():
    """Return the full list of referral FAQs."""
    return {"faqs": REFERRAL_FAQS}

@router.get("/referral-rules")
async def get_rules():
    """Return the list of referral rules."""
    return {"rules": REFERRAL_RULES}