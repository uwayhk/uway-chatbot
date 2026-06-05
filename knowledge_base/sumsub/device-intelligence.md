---
source: sumsub
original_url: https://docs.sumsub.com/docs/device-intelligence
scraped_at: 2026-05-02T11:01:48.701804
---

# Sumsub: Device Intelligence

Title: Device Intelligence

URL Source: https://docs.sumsub.com/docs/device-intelligence

Markdown Content:
Device Intelligence is a powerful set of tools that enables the detection and analysis of device-based signals during verification, financial transactions and user interactions with the platform (sign-ups, logins, resetting passwords, and other significant actions). By identifying the specific devices interacting with your platform, it uncovers risky patterns that may indicate fraudulent behavior. These patterns include:

*   Account takeover
*   Multi-accounting schemes
*   Bot activity
*   Account sharing

Device Intelligence is particularly effective at identifying sophisticated fraud attempts such as using spoofed or emulated devices, operating in incognito or privacy modes, running on rooted/jailbroken devices, using VPN applications, or attempting to spoof location. By flagging anomalies early, organizations can respond proactively, blocking high-risk activity before it escalates, and allow genuine users to proceed without unnecessary friction.

Device Intelligence serves two core purposes:

*   **Reliable device identification**. This service generates stable, unique device identifiers that persist across sessions and, for mobile devices, across app reinstallation.
*   **Suspicious environment detection**. Device Intelligence identifies signs of tampered, emulated, or manipulated device environments that may indicate fraud attempts.

When integrated with verification procedures, [Transaction Monitoring](https://docs.sumsub.com/docs/transaction-monitoring), and other [Fraud Prevention controls](https://docs.sumsub.com/docs/about-fraud-prevention), Device Intelligence delivers a balance of security and usability, empowering businesses to protect their platforms without compromising the experience of legitimate users.

Device Intelligence is powered by [Fingerprint](https://fingerprint.com/), a leading provider of advanced device identification technology. The system uses techniques for capturing low-level browser and device signals – for instance, device fingerprinting, which is one of the many techniques used in Device Intelligence. These methods work together with the goal of generating a stable, unique device identifier and detecting suspicious device activity such as:

*   Bot activity detection
*   VPN and proxy usage
*   Device spoofing and emulation
*   Privacy-focused software and incognito modes
*   Rooted/jailbroken devices
*   Location spoofing

This identifier remains consistent even if the user changes browser settings, clears cookies, or uses incognito mode.

The entire process of collecting device information happens immediately upon device access and does not require continuous tracking of user interactions with the platform. Importantly, this operates without requiring user permissions, meaning no intrusive prompts or interruptions for your users.

Device Intelligence works differently depending on the platform. Understanding these differences will help you interpret device data correctly and tailor your risk response accordingly.

In the following table, you can find a comparison of Web Device Intelligence and Mobile Device Intelligence across its key aspects.

| Aspect | Web Device Intelligence | Mobile Device Intelligence |
| --- | --- | --- |
| Device ID representation | Browser instance | Physical device |
| Identification method | Probabilistic (fingerprinting) | Deterministic (hardware-level signals) |
| ID persistence | Stable identifier even when cookies are cleared or browser storage is reset | Persists across app reinstall and data clear |
| Multiple browsers/apps | Different browsers -> Different IDs | Same device -> Same ID regardless of app |
| Collision probability | Low but non-zero | No practical collisions |
| Accuracy | High | Very high (no false positives) |

**Web Device Intelligence** works via:

*   **WebSDK** – for verification flows.
*   **JS SDK** – for pre-KYC/sign-up pre-screening and Behavior Monitoring.

It works in desktop and mobile browsers, and WebViews inside mobile apps.

**Mobile Device Intelligence** works via native SDKs:

*   [iOS SDK](https://docs.sumsub.com/docs/get-started-ios)
*   [Android SDK](https://docs.sumsub.com/docs/get-started-android)

> 📘
> Device Intelligence requires MobileSDK integration in your app. Also, its module has to be enabled for Android and iOS.

Device IDs provide a more stable and precise way to identify returning devices than IP addresses, enabling more reliable risk decisions even when networks change or traffic is routed through VPNs or proxies.

IP addresses are unreliable for device identification because they:

*   Change frequently (mobile networks, ISP reassignment).
*   Are shared across multiple users and devices (NAT, corporate networks).
*   Can be easily masked using VPNs or proxies.

Device Intelligence device IDs overcome these limitations as they are:

*   Stable across network changes.
*   Device-specific (not shared).
*   Independent of IP rotation or VPN usage.

They also provide much higher precision and lower collision rates.

Device Intelligence integration operates across key touchpoints in both **verification flow** and **Transaction Monitoring processes**, ensuring risk detection throughout the user journey.

It operates across three stages: **capturing device data**, **assessing risk**, and **taking decisions**.

At this stage, Device Intelligence workflow depends on the verification stage or service you use:

| Stage | Method | SDK |
| --- | --- | --- |
| Verification | Automatically during verification flow | WebSDK 2.0, MobileSDK |
| Pre-KYC onboarding/sign-up pre-screening | Via [JS SDK and Sumsub API](https://docs.sumsub.com/reference/use-device-intelligence-for-pre-kyc-check) | JS SDK, MobileSDK (experimental) |
| Behavior Monitoring | Linked to user activity (logins, password changes) | JS SDK, MobileSDK (experimental) |
| Transaction Monitoring | Linked to financial transactions | JS SDK, MobileSDK (experimental) |

Device data feeds into multiple risk assessment mechanisms:

*   [Behavior Monitoring](https://docs.sumsub.com/docs/behavior-monitoring) – links devices to user activity patterns to detect anomalies.
*   Transaction Monitoring – links devices to financial transactions for fraud detection.
*   [Applicant Risk Scoring](https://docs.sumsub.com/docs/applicant-risk-scoring) – calculates comprehensive risk scores using device signals combined with other factors.

> 👍
> When applying Applicant Risk Scoring, combine other risk sources like [email/phone risk assessment](https://docs.sumsub.com/docs/digital-footprint-checks), risk labels, custom transaction monitoring and verification rules, with device signals for comprehensive risk assessment. You can use the following device signals:
> 
> 
> *   Device risk labels
> *   Reused devices
> *   New devices
> *   Multiple devices per session
> 
> 
> Based on risk scores, trigger appropriate responses:
> 
> 
> *   Enable step-up checks.
> *   Route a case to Case Management for manual review.
> *   Enable enhanced monitoring by flagging a case for ongoing observation.

Based on risk assessment, decisions can be made through:

*   [Workflow Builder](https://docs.sumsub.com/docs/workflow-builder) – automate verification decisions based on device signals.
*   [Transaction Monitoring rules engine](https://docs.sumsub.com/docs/tm-rules) – define rules that trigger actions based on device risk.
*   [Case Management](https://docs.sumsub.com/docs/case-management) – route flagged applicants for manual review.
*   [Applicant actions](https://docs.sumsub.com/docs/applicant-actions) – apply actions directly to applicants based on device data.
*   [Blocklists](https://docs.sumsub.com/docs/blocklist-applicants) – block high-risk applicants from future interactions.

The table below outlines the risk signals detected by the Device intelligence solution across different platforms and environments.

| Name of signal | Web, Desktop | Web, Android | Web, iOS | Mobile Apps, Android | Mobile Apps, iOS |
| --- | --- | --- | --- | --- | --- |
| Browser ID | ✔ | ✔ | ✔ | ✖ | ✖ |
| Device ID | ✖ | ✖ | ✖ | ✔ | ✔ |
| Browser Name | ✔ | ✔ | ✔ | ✖ | ✖ |
| Operational system | ✔ | ✔ | ✔ | ✖ | ✖ |
| Device Model | ✖ | ✔ | ✖ | ✔ | ✖ |
| Device Type | ✔ | ✔ | ✔ | ✔ | ✔ |
| IP Address | ✔ | ✔ | ✔ | ✔ | ✔ |
| IP Autonomous System Number (ASN) | ✔ | ✔ | ✔ | ✔ | ✔ |
| IP Network Type (Residential, Mobile, Hosting, VPN, ect) | ✔ | ✔ | ✔ | ✔ | ✔ |
| VPN Provider | ✔ | ✔ | ✔ | ✔ | ✔ |
| IP Geolocation (coordinates, confidence radius in km) | ✔ | ✔ | ✔ | ✔ | ✔ |
| Browser Automation Detection (AI Agents, Malicious Bots, tools like Puppeteer and Playwright) | ✔ | ✔ | ✔ | ✖ | ✖ |
| Privacy-Focused Browsers (Brave, Tor Browser, etc.) | ✔ | ✔ | ✔ | ✖ | ✖ |
| Incognito Mode | ✔ | ✔ | ✔ | ✖ | ✖ |
| Browser Tampering (Spoofing) | ✔ | ✔ | ✔ | ✖ | ✖ |
| Virtual Machine | ✔ | ✔ | ✔ | ✖ | ✖ |
| Developer Tools | ✔ | ✔ | ✔ | ✖ | ✖ |
| Recent Factory Reset | ✖ | ✖ | ✖ | ✔ | ✔ |
| Mobile VPN | ✖ | ✖ | ✖ | ✔ | ✔ |
| Geolocation Spoofing | ✖ | ✖ | ✖ | ✔ | ✔ |
| Tampered Request Detection | ✖ | ✖ | ✖ | ✔ | ✔ |
| Android Emulator | ✖ | ✖ | ✖ | ✔ | ✖ |
| Jailbroken Device | ✖ | ✖ | ✖ | ✖ | ✔ |
| MitM Attack | ✖ | ✖ | ✖ | ✔ | ✔ |
| Frida Detection | ✖ | ✖ | ✖ | ✔ | ✔ |
| Rooted Device | ✖ | ✖ | ✖ | ✔ | ✖ |
| Cloned App Detection | ✖ | ✖ | ✖ | ✔ | ✖ |

Device Intelligence supports [risk labels](https://docs.sumsub.com/docs/applicant-risk-labels#device-risk-labels) across web and mobile platforms.

Device Intelligence also includes all signals from the Advanced IP Check module. For the complete list of IP-based signals, refer to [this article](https://docs.sumsub.com/docs/advanced-ip-check#advanced-ip-check-risk-labels).

To enable Device Intelligence for your account, contact your Customer Success Manager or enable it yourself if you are a [self-service](https://docs.sumsub.com/docs/self-service) client.

> 👍
> You can test your Device Intelligence integration by using Simulation. For more instructions on how to enable it, see [this article](https://docs.sumsub.com/reference/enable-device-intelligence-simulation).

Complete the following actions to enable Device Intelligence during the onboarding process. The enablement process is the same for both WebSDK and MobileSDK verification flows.

1.   Enable Device Intelligence module (MobileSDK integration): 
    *   For [iOS](https://docs.sumsub.com/docs/get-started-ios#device-intelligence)
    *   For [Android](https://docs.sumsub.com/docs/get-started-android#device-intelligence)

2.   In the Dashboard, go to **Integrations** and select the level of interest.
3.   Open the **Verification Level** settings.
4.   In the **Configurations** section, open the **Fraud prevention** tab and select the **Capture devices** checkbox.

This enables the system to automatically collect device signals when users begin the verification process.

Note that device capture is:

*   Invisible to the end user.
*   Does not affect user experience.
*   Does not introduce noticeable latency.

> ❗️
> The system collects device data **only when both** of the following conditions are met:
> 
> 
> *   The device capture is enabled for the verification level.
> *   The verification session is completed.

You can leverage Device Intelligence for Ongoing Monitoring by linking device data to specific events, such as logins, password changes, and financial transactions.

*   To enable **web Device Intelligence** for Behavior Monitoring and Transaction Monitoring, integrate the JS SDK and Sumsub API on your application frontend to collect device data and link it to behavioral events.

 For more information on how to integrate with Device Intelligence, see [this article](https://docs.sumsub.com/reference/get-started-with-device-intelligence).
*   To enable **mobile Device Intelligence** for Behavior Monitoring and Transaction Monitoring, contact your Customer Success Manager about native SDK integration options for mobile Behavior Monitoring.

Device analytics can help identify patterns of suspicious activity, such as device re-use, high-risk configurations, or abnormal login behavior, across your user base. These insights support manual investigations and inform risk-based decisions without disrupting legitimate users.

You can view both the **Devices** and **Device analytics** in the **Device Intelligence** section in the Dashboard:

*   **Devices** section contains a list of all detected devices with their general information and risk labels.
*   **Device analytics** displays graphs showing the total number of devices, login attempts, and the number of risk labels, as well as a world map showing the device geolocation.

Device data is collected and available in real time. You can access it from multiple locations:

*   In the Dashboard, go to the **Device Intelligence** section to view all devices and analytics. To monitor monitor device-specific activity, select the device of interest.
*   When viewing **verification**, a **Device Check** block appears in completed verifications, showing device information and any detected risk labels.
*   On the **applicant profile**, the **Devices** tab lists: 
    *   All devices associated with the applicant.
    *   Suspicious labels highlighting device risks.

*   From the **Overview** on the applicant page. In the Dashboard, navigate to the **Applicants** section and select the applicant of interest. On the **Overview** tab, scroll down to the **Devices** section.
*   From the **Transactions** page. In the Dashboard, go to the **Transactions and Travel Rule** and select the transaction of interest. Scroll down to the **Transaction antifraud** section and click **View device details** in the **Device** info.

Device signals are **risk indicators**, not definitive proof of fraud. You should use it as part of a broader risk assessment strategy.

When the same Device ID appears across multiple applicants, it may indicate:

Risk scenarios*   Multi-accounting

*   Bonus/referral abuse

*   Trial abuse

*   Account farming

*   Money muling

*   Fraud networks/fraud rings
Legitimate scenarios*   Duplicate accounts are allowed by policy.

*   Users register across isolated projects.

*   Family members share a device.

*   Employees assist users from a shared device.

*   Offline/in-person verification is performed.

> 📘
> Device reuse is a **risk signal, not proof of fraud**. Risk increases with the **number of applicants** sharing the device and speed/velocity of reuse (many accounts in a short time).

When new device IDs appear for an applicant, or multiple device IDs are observed within a single session, it may indicate:

Risk scenarios*   Multiple devices used within a single session may indicate third-party account creation.

*   Appearance of new devices may indicate:

    *   Account takeover
    *   Account transfer to unverified users
    *   Shared account usage
Legitimate scenarios*   Users changing or upgrading devices is a normal behavior.

> 📘
> Apply automated blocking or rejection **only** in high-confidence and high-risk scenarios:
> 
> 
> *   Large-scale fraud attacks
> *   Clear policy violations with multiple confirming signals

Prefer setting up additional verification steps rather than outright blocking. Enable the following checks to secure your verification flow:

*   [Liveness and Face match](https://docs.sumsub.com/docs/liveness)
*   [Email and phone verification](https://docs.sumsub.com/docs/email-and-phone-verification)
*   [Payment Method Check Advanced](https://docs.sumsub.com/docs/payment-method-check-advanced)
*   [Questionnaire](https://docs.sumsub.com/docs/questionnaire)

If you already have an active contract with [Fingerprint Pro](https://fingerprint.com/), Sumsub supports a Bring Your Own Key integration that allows you to:

*   **Capture and utilize devices within Sumsub-controlled flows** — within the Sumsub **WebSDK** and **MobileSDK** verification flows, device signals are collected using your Fingerprint Pro credentials and linked to the applicant profile on the Sumsub side.
*   **Link devices you are already collecting** — use Fingerprint data you collect across your platform (for instance, at sign up, login or financial transaction) within the following Sumsub solutions: 
    *   [Transaction Monitoring](https://docs.sumsub.com/docs/transaction-monitoring)
    *   [Behavior Monitoring](https://docs.sumsub.com/docs/behavior-monitoring)
    *   [Rules engine](https://docs.sumsub.com/docs/tm-rules)
    *   [Workflow Builder](https://docs.sumsub.com/docs/workflow-builder)
    *   [Applicant risk scoring](https://docs.sumsub.com/docs/applicant-risk-scoring)

> 📘
> To enable BYOK for your account, contact your **Sumsub representative**.

Updated about 1 month ago

* * *

Did this page help you?

*       *   [How Device Intelligence works](https://docs.sumsub.com/docs/device-intelligence#how-device-intelligence-works)
    *           *   [Web and mobile Device Intelligence](https://docs.sumsub.com/docs/device-intelligence#web-and-mobile-device-intelligence)
        *   [Benefits of device ID](https://docs.sumsub.com/docs/device-intelligence#benefits-of-device-id)
        *   [Where Device Intelligence works](https://docs.sumsub.com/docs/device-intelligence#where-device-intelligence-works)
        *   [Device Intelligence data and risk signals](https://docs.sumsub.com/docs/device-intelligence#device-intelligence-data-and-risk-signals)
        *   [Risk labels](https://docs.sumsub.com/docs/device-intelligence#risk-labels)

    *   [How to enable Device Intelligence](https://docs.sumsub.com/docs/device-intelligence#how-to-enable-device-intelligence)
    *           *   [Enable Device Intelligence for verification](https://docs.sumsub.com/docs/device-intelligence#enable-device-intelligence-for-verification)
        *   [Enable Device Intelligence for Behavior Monitoring and Transaction Monitoring](https://docs.sumsub.com/docs/device-intelligence#enable-device-intelligence-for-behavior-monitoring-and-transaction-monitoring)

    *   [How to use Device Intelligence](https://docs.sumsub.com/docs/device-intelligence#how-to-use-device-intelligence)
    *           *   [View devices and device analytics](https://docs.sumsub.com/docs/device-intelligence#view-devices-and-device-analytics)
        *   [View device data](https://docs.sumsub.com/docs/device-intelligence#view-device-data)
        *   [Interpret device signals](https://docs.sumsub.com/docs/device-intelligence#interpret-device-signals)

    *   [Device Intelligence — Bring Your Own Key (BYOK)](https://docs.sumsub.com/docs/device-intelligence#device-intelligence--bring-your-own-key-byok)
