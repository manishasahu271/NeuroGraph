from __future__ import annotations

# Comprehensive seed dataset (as provided in the prompt).

BIOMARKERS = [
    {
        "name": "typing_speed_decline",
        "category": "motor",
        "source": "smartphone_keyboard",
        "description": "Measurable decrease in typing speed and increase in error rate over time",
    },
    {
        "name": "typing_error_increase",
        "category": "motor",
        "source": "smartphone_keyboard",
        "description": "Higher frequency of typos, autocorrect usage, and backspace presses",
    },
    {
        "name": "sleep_fragmentation",
        "category": "sleep",
        "source": "accelerometer",
        "description": "Increased nighttime awakenings and reduced sleep continuity via phone movement",
    },
    {
        "name": "sleep_onset_delay",
        "category": "sleep",
        "source": "screen_activity",
        "description": "Later bedtime detected by phone screen-off time shifting progressively later",
    },
    {
        "name": "reduced_daily_mobility",
        "category": "motor",
        "source": "gps_accelerometer",
        "description": "Decrease in daily step count and radius of movement from GPS data",
    },
    {
        "name": "gait_irregularity",
        "category": "motor",
        "source": "accelerometer",
        "description": "Increased variability in walking patterns detected by phone accelerometer",
    },
    {
        "name": "increased_app_switching",
        "category": "digital_behavior",
        "source": "screen_activity",
        "description": "Higher frequency of switching between apps without completing tasks",
    },
    {
        "name": "scrolling_passivity_increase",
        "category": "digital_behavior",
        "source": "screen_activity",
        "description": "Increase in passive scrolling time vs active creation or communication",
    },
    {
        "name": "screen_time_spike",
        "category": "digital_behavior",
        "source": "screen_activity",
        "description": "Sudden increase in total daily screen time beyond personal baseline",
    },
    {
        "name": "social_interaction_decline",
        "category": "social",
        "source": "call_message_logs",
        "description": "Reduced call frequency, longer message response times, fewer unique contacts",
    },
    {
        "name": "voice_prosody_change",
        "category": "speech",
        "source": "microphone",
        "description": "Changes in speech rate, pitch variability, and pause patterns",
    },
    {
        "name": "word_finding_pauses",
        "category": "speech",
        "source": "microphone",
        "description": "Increased mid-sentence pauses suggesting word retrieval difficulty",
    },
    {
        "name": "circadian_rhythm_shift",
        "category": "sleep",
        "source": "screen_activity",
        "description": "Shift in peak phone usage hours indicating disrupted sleep-wake cycle",
    },
    {
        "name": "location_entropy_decrease",
        "category": "motor",
        "source": "gps",
        "description": "Visiting fewer unique locations, more time at home",
    },
    {
        "name": "response_time_increase",
        "category": "digital_behavior",
        "source": "notifications",
        "description": "Longer time to respond to messages, emails, and notifications",
    },
    {
        "name": "phone_unlock_frequency_change",
        "category": "digital_behavior",
        "source": "screen_activity",
        "description": "Abnormal change in phone check/unlock frequency indicating restlessness or disengagement",
    },
    {
        "name": "exercise_decline",
        "category": "motor",
        "source": "accelerometer",
        "description": "Reduction in detected physical activity sessions and intensity",
    },
    {
        "name": "heart_rate_variability_decrease",
        "category": "motor",
        "source": "smartwatch",
        "description": "Reduced HRV indicating increased stress or autonomic dysfunction",
    },
    {
        "name": "nighttime_phone_usage",
        "category": "sleep",
        "source": "screen_activity",
        "description": "Increased phone usage between 12am-5am indicating sleep disruption",
    },
    {
        "name": "keystroke_rhythm_irregularity",
        "category": "motor",
        "source": "smartphone_keyboard",
        "description": "Increased variability in time between keystrokes suggesting motor or attention issues",
    },
]

SYMPTOMS = [
    {
        "name": "memory_lapses",
        "severity_range": "mild-severe",
        "description": "Difficulty remembering recent events, names, or appointments",
    },
    {
        "name": "attention_deficit",
        "severity_range": "mild-moderate",
        "description": "Reduced ability to maintain focus on tasks or conversations",
    },
    {
        "name": "mood_changes",
        "severity_range": "mild-severe",
        "description": "Unexplained shifts in mood including irritability and sadness",
    },
    {
        "name": "fatigue",
        "severity_range": "mild-severe",
        "description": "Persistent tiredness not explained by physical exertion",
    },
    {
        "name": "word_finding_difficulty",
        "severity_range": "mild-moderate",
        "description": "Trouble finding the right words during conversation",
    },
    {
        "name": "social_withdrawal",
        "severity_range": "mild-severe",
        "description": "Reduced interest in social activities and relationships",
    },
    {
        "name": "executive_function_decline",
        "severity_range": "mild-severe",
        "description": "Difficulty with planning, organizing, and completing multi-step tasks",
    },
    {
        "name": "spatial_disorientation",
        "severity_range": "moderate-severe",
        "description": "Getting lost in familiar places or difficulty navigating",
    },
    {
        "name": "sleep_disturbance",
        "severity_range": "mild-severe",
        "description": "Difficulty falling asleep, staying asleep, or non-restorative sleep",
    },
    {
        "name": "psychomotor_slowing",
        "severity_range": "mild-moderate",
        "description": "Slowed physical movements and reaction times",
    },
    {
        "name": "anhedonia",
        "severity_range": "mild-severe",
        "description": "Loss of interest or pleasure in previously enjoyed activities",
    },
    {
        "name": "concentration_difficulty",
        "severity_range": "mild-severe",
        "description": "Trouble concentrating on reading, conversations, or work tasks",
    },
    {
        "name": "decision_making_difficulty",
        "severity_range": "mild-moderate",
        "description": "Increased difficulty making everyday decisions",
    },
    {
        "name": "emotional_blunting",
        "severity_range": "moderate-severe",
        "description": "Reduced emotional responsiveness and flat affect",
    },
    {
        "name": "restlessness",
        "severity_range": "mild-moderate",
        "description": "Inability to sit still, constant fidgeting, inner sense of agitation",
    },
]

CONDITIONS = [
    {
        "name": "mild_cognitive_impairment",
        "icd_code": "G31.84",
        "severity": "moderate",
        "description": "Noticeable cognitive decline greater than expected for age but not dementia",
    },
    {
        "name": "early_alzheimer_disease",
        "icd_code": "G30.9",
        "severity": "severe",
        "description": "Progressive neurodegenerative disorder with memory loss and cognitive decline",
    },
    {
        "name": "major_depressive_disorder",
        "icd_code": "F33",
        "severity": "severe",
        "description": "Persistent depressed mood with loss of interest affecting daily functioning",
    },
    {
        "name": "generalized_anxiety_disorder",
        "icd_code": "F41.1",
        "severity": "moderate",
        "description": "Excessive worry and anxiety about everyday matters",
    },
    {
        "name": "burnout_syndrome",
        "icd_code": "QD85",
        "severity": "moderate",
        "description": "Chronic workplace stress resulting in exhaustion and reduced efficacy",
    },
    {
        "name": "chronic_fatigue_syndrome",
        "icd_code": "R53.82",
        "severity": "moderate",
        "description": "Persistent fatigue not relieved by rest lasting 6+ months",
    },
    {
        "name": "insomnia_disorder",
        "icd_code": "G47.0",
        "severity": "moderate",
        "description": "Persistent difficulty initiating or maintaining sleep",
    },
    {
        "name": "adhd_adult",
        "icd_code": "F90.0",
        "severity": "moderate",
        "description": "Attention deficit hyperactivity disorder persisting into adulthood",
    },
    {
        "name": "early_parkinson_disease",
        "icd_code": "G20",
        "severity": "severe",
        "description": "Progressive nervous system disorder affecting movement",
    },
    {
        "name": "post_concussion_syndrome",
        "icd_code": "F07.81",
        "severity": "moderate",
        "description": "Persistent symptoms following traumatic brain injury",
    },
]

CLINICAL_EVIDENCE = [
    {
        "title": "AI and Wearables for Early Detection of Cognitive Impairment and Dementia",
        "doi": "10.2196/86262",
        "year": 2026,
        "journal": "J Med Internet Res",
        "summary": "Systematic review of 49 studies finding continuous passive monitoring from wearables detects subtle behavioral changes supporting earlier cognitive decline detection",
        "sample_size": "49 studies",
        "confidence": 0.92,
    },
    {
        "title": "Deep Learning Detection of Cognitive Impairment from Passive Smartphone Sensing",
        "doi": "10.48550/arXiv.2509.23158",
        "year": 2025,
        "journal": "arXiv",
        "summary": "Used 30-day sliding windows of passive smartphone features to detect cognitive impairment in community-dwelling older adults",
        "sample_size": "multi-year cohort",
        "confidence": 0.87,
    },
    {
        "title": "Smartwatch and Smartphone Based Detection of Mild Cognitive Impairment",
        "doi": "10.1038/s41591-025-03468-w",
        "year": 2025,
        "journal": "Nature Medicine",
        "summary": "Demonstrated smartwatch and smartphone data can remotely detect mild cognitive impairment with clinical-grade accuracy",
        "sample_size": "large multi-site",
        "confidence": 0.94,
    },
    {
        "title": "Voiceprints of Cognitive Impairment: Analyzing Digital Voice",
        "doi": "10.1038/s44400-025-00040-0",
        "year": 2025,
        "journal": "npj Dementia",
        "summary": "AI analysis of voice recordings achieved AUC of 0.988 for detecting cognitive impairment from speech patterns",
        "sample_size": "120 patients, 68 controls",
        "confidence": 0.95,
    },
    {
        "title": "Gait Analysis Using Wearable Sensors Predicts Cognitive Decline",
        "doi": "10.1038/s43587-021-00040-w",
        "year": 2021,
        "journal": "Nature Aging",
        "summary": "Wearable sensor gait analysis predicts cognitive decline in older adults before clinical symptoms",
        "sample_size": "prospective cohort",
        "confidence": 0.88,
    },
    {
        "title": "Continuous Monitoring of Smartphone Use Patterns for Early Detection",
        "doi": "10.1177/20552076221089092",
        "year": 2022,
        "journal": "Digital Health Journal",
        "summary": "Large-scale study showing smartphone usage patterns correlate with early cognitive changes",
        "sample_size": "large-scale",
        "confidence": 0.85,
    },
    {
        "title": "Keystroke Dynamics as Digital Biomarker for Cognitive Frailty",
        "doi": "10.3389/fnagi.2023.1168468",
        "year": 2023,
        "journal": "Frontiers in Aging Neuroscience",
        "summary": "Typing patterns on smartphones can serve as passive digital biomarkers for cognitive frailty",
        "sample_size": "clinical study",
        "confidence": 0.83,
    },
    {
        "title": "Sleep Disruption as Digital Biomarker for Neurodegeneration",
        "doi": "10.1016/j.sleep.2023.05.012",
        "year": 2023,
        "journal": "Sleep Medicine",
        "summary": "Phone-detected sleep fragmentation patterns correlate with neurodegenerative biomarkers",
        "sample_size": "multi-center",
        "confidence": 0.86,
    },
    {
        "title": "Social Isolation Measured via Smartphone as Predictor of Depression",
        "doi": "10.1038/s41746-023-00765-z",
        "year": 2023,
        "journal": "npj Digital Medicine",
        "summary": "Smartphone-measured social interaction decline predicts onset of depressive episodes",
        "sample_size": "longitudinal cohort",
        "confidence": 0.89,
    },
    {
        "title": "Digital Phenotyping for Early Detection of Burnout",
        "doi": "10.1093/jamia/ocac042",
        "year": 2022,
        "journal": "JAMIA",
        "summary": "Phone usage patterns including screen time spikes and circadian disruption predict burnout onset",
        "sample_size": "workplace cohort",
        "confidence": 0.81,
    },
    {
        "title": "Heart Rate Variability from Wearables Predicts Cognitive Aging",
        "doi": "10.1111/psyp.14228",
        "year": 2023,
        "journal": "Psychophysiology",
        "summary": "Reduced HRV measured by consumer wearables associated with accelerated cognitive aging",
        "sample_size": "aging cohort",
        "confidence": 0.84,
    },
    {
        "title": "App Usage Patterns and Attention in Adults with ADHD",
        "doi": "10.1177/10870547231162",
        "year": 2023,
        "journal": "J Attention Disorders",
        "summary": "Rapid app switching and short session durations on smartphones correlate with ADHD symptom severity",
        "sample_size": "clinical + controls",
        "confidence": 0.82,
    },
]

RISK_FACTORS = [
    {"name": "age_over_65", "category": "demographic", "modifiable": False},
    {"name": "sleep_deprivation_chronic", "category": "lifestyle", "modifiable": True},
    {"name": "sedentary_lifestyle", "category": "lifestyle", "modifiable": True},
    {"name": "chronic_high_stress", "category": "lifestyle", "modifiable": True},
    {"name": "social_isolation", "category": "social", "modifiable": True},
    {"name": "family_history_dementia", "category": "genetic", "modifiable": False},
    {"name": "traumatic_brain_injury", "category": "medical", "modifiable": False},
    {"name": "excessive_screen_time", "category": "lifestyle", "modifiable": True},
]

# RELATIONSHIPS — (source_name, relationship_type, target_name, properties)

INDICATES_RELS = [
    ("typing_speed_decline", "INDICATES", "psychomotor_slowing", {"strength": 0.82, "evidence_count": 5}),
    ("typing_speed_decline", "INDICATES", "attention_deficit", {"strength": 0.75, "evidence_count": 3}),
    ("typing_error_increase", "INDICATES", "attention_deficit", {"strength": 0.78, "evidence_count": 4}),
    ("typing_error_increase", "INDICATES", "memory_lapses", {"strength": 0.65, "evidence_count": 2}),
    ("sleep_fragmentation", "INDICATES", "fatigue", {"strength": 0.91, "evidence_count": 8}),
    ("sleep_fragmentation", "INDICATES", "concentration_difficulty", {"strength": 0.79, "evidence_count": 5}),
    ("sleep_fragmentation", "INDICATES", "mood_changes", {"strength": 0.73, "evidence_count": 4}),
    ("sleep_onset_delay", "INDICATES", "sleep_disturbance", {"strength": 0.88, "evidence_count": 6}),
    ("reduced_daily_mobility", "INDICATES", "fatigue", {"strength": 0.80, "evidence_count": 5}),
    ("reduced_daily_mobility", "INDICATES", "social_withdrawal", {"strength": 0.72, "evidence_count": 3}),
    ("gait_irregularity", "INDICATES", "psychomotor_slowing", {"strength": 0.85, "evidence_count": 6}),
    ("gait_irregularity", "INDICATES", "spatial_disorientation", {"strength": 0.68, "evidence_count": 3}),
    ("increased_app_switching", "INDICATES", "attention_deficit", {"strength": 0.84, "evidence_count": 5}),
    ("increased_app_switching", "INDICATES", "restlessness", {"strength": 0.76, "evidence_count": 3}),
    ("scrolling_passivity_increase", "INDICATES", "anhedonia", {"strength": 0.77, "evidence_count": 4}),
    ("scrolling_passivity_increase", "INDICATES", "fatigue", {"strength": 0.69, "evidence_count": 3}),
    ("screen_time_spike", "INDICATES", "sleep_disturbance", {"strength": 0.74, "evidence_count": 4}),
    ("screen_time_spike", "INDICATES", "concentration_difficulty", {"strength": 0.71, "evidence_count": 3}),
    ("social_interaction_decline", "INDICATES", "social_withdrawal", {"strength": 0.90, "evidence_count": 7}),
    ("social_interaction_decline", "INDICATES", "mood_changes", {"strength": 0.82, "evidence_count": 5}),
    ("voice_prosody_change", "INDICATES", "emotional_blunting", {"strength": 0.79, "evidence_count": 4}),
    ("voice_prosody_change", "INDICATES", "mood_changes", {"strength": 0.81, "evidence_count": 5}),
    ("word_finding_pauses", "INDICATES", "word_finding_difficulty", {"strength": 0.92, "evidence_count": 7}),
    ("word_finding_pauses", "INDICATES", "memory_lapses", {"strength": 0.76, "evidence_count": 4}),
    ("circadian_rhythm_shift", "INDICATES", "sleep_disturbance", {"strength": 0.87, "evidence_count": 6}),
    ("location_entropy_decrease", "INDICATES", "social_withdrawal", {"strength": 0.78, "evidence_count": 4}),
    ("location_entropy_decrease", "INDICATES", "fatigue", {"strength": 0.70, "evidence_count": 3}),
    ("response_time_increase", "INDICATES", "psychomotor_slowing", {"strength": 0.77, "evidence_count": 4}),
    ("response_time_increase", "INDICATES", "attention_deficit", {"strength": 0.73, "evidence_count": 3}),
    ("phone_unlock_frequency_change", "INDICATES", "restlessness", {"strength": 0.72, "evidence_count": 3}),
    ("exercise_decline", "INDICATES", "fatigue", {"strength": 0.83, "evidence_count": 5}),
    ("exercise_decline", "INDICATES", "mood_changes", {"strength": 0.75, "evidence_count": 4}),
    ("heart_rate_variability_decrease", "INDICATES", "fatigue", {"strength": 0.78, "evidence_count": 4}),
    ("nighttime_phone_usage", "INDICATES", "sleep_disturbance", {"strength": 0.86, "evidence_count": 5}),
    ("keystroke_rhythm_irregularity", "INDICATES", "psychomotor_slowing", {"strength": 0.80, "evidence_count": 4}),
    ("keystroke_rhythm_irregularity", "INDICATES", "attention_deficit", {"strength": 0.74, "evidence_count": 3}),
]

ASSOCIATED_WITH_RELS = [
    ("memory_lapses", "ASSOCIATED_WITH", "mild_cognitive_impairment", {"correlation": 0.88}),
    ("memory_lapses", "ASSOCIATED_WITH", "early_alzheimer_disease", {"correlation": 0.92}),
    ("attention_deficit", "ASSOCIATED_WITH", "adhd_adult", {"correlation": 0.87}),
    ("attention_deficit", "ASSOCIATED_WITH", "burnout_syndrome", {"correlation": 0.74}),
    ("mood_changes", "ASSOCIATED_WITH", "major_depressive_disorder", {"correlation": 0.86}),
    ("mood_changes", "ASSOCIATED_WITH", "generalized_anxiety_disorder", {"correlation": 0.79}),
    ("fatigue", "ASSOCIATED_WITH", "burnout_syndrome", {"correlation": 0.91}),
    ("fatigue", "ASSOCIATED_WITH", "chronic_fatigue_syndrome", {"correlation": 0.93}),
    ("fatigue", "ASSOCIATED_WITH", "major_depressive_disorder", {"correlation": 0.82}),
    ("word_finding_difficulty", "ASSOCIATED_WITH", "mild_cognitive_impairment", {"correlation": 0.84}),
    ("word_finding_difficulty", "ASSOCIATED_WITH", "early_alzheimer_disease", {"correlation": 0.89}),
    ("social_withdrawal", "ASSOCIATED_WITH", "major_depressive_disorder", {"correlation": 0.88}),
    ("social_withdrawal", "ASSOCIATED_WITH", "early_alzheimer_disease", {"correlation": 0.72}),
    ("executive_function_decline", "ASSOCIATED_WITH", "mild_cognitive_impairment", {"correlation": 0.86}),
    ("executive_function_decline", "ASSOCIATED_WITH", "adhd_adult", {"correlation": 0.78}),
    ("spatial_disorientation", "ASSOCIATED_WITH", "early_alzheimer_disease", {"correlation": 0.91}),
    ("sleep_disturbance", "ASSOCIATED_WITH", "insomnia_disorder", {"correlation": 0.94}),
    ("sleep_disturbance", "ASSOCIATED_WITH", "generalized_anxiety_disorder", {"correlation": 0.76}),
    ("psychomotor_slowing", "ASSOCIATED_WITH", "early_parkinson_disease", {"correlation": 0.88}),
    ("psychomotor_slowing", "ASSOCIATED_WITH", "major_depressive_disorder", {"correlation": 0.74}),
    ("anhedonia", "ASSOCIATED_WITH", "major_depressive_disorder", {"correlation": 0.90}),
    ("anhedonia", "ASSOCIATED_WITH", "burnout_syndrome", {"correlation": 0.77}),
    ("concentration_difficulty", "ASSOCIATED_WITH", "adhd_adult", {"correlation": 0.89}),
    ("concentration_difficulty", "ASSOCIATED_WITH", "burnout_syndrome", {"correlation": 0.80}),
    ("decision_making_difficulty", "ASSOCIATED_WITH", "mild_cognitive_impairment", {"correlation": 0.79}),
    ("emotional_blunting", "ASSOCIATED_WITH", "major_depressive_disorder", {"correlation": 0.83}),
    ("restlessness", "ASSOCIATED_WITH", "generalized_anxiety_disorder", {"correlation": 0.85}),
    ("restlessness", "ASSOCIATED_WITH", "adhd_adult", {"correlation": 0.82}),
]

COMORBID_RELS = [
    ("major_depressive_disorder", "COMORBID_WITH", "generalized_anxiety_disorder", {"prevalence": 0.60}),
    ("major_depressive_disorder", "COMORBID_WITH", "insomnia_disorder", {"prevalence": 0.75}),
    ("burnout_syndrome", "COMORBID_WITH", "insomnia_disorder", {"prevalence": 0.55}),
    ("mild_cognitive_impairment", "COMORBID_WITH", "major_depressive_disorder", {"prevalence": 0.40}),
    ("early_alzheimer_disease", "COMORBID_WITH", "insomnia_disorder", {"prevalence": 0.45}),
    ("adhd_adult", "COMORBID_WITH", "generalized_anxiety_disorder", {"prevalence": 0.50}),
]

RISK_FACTOR_RELS = [
    ("age_over_65", "INCREASES_RISK_OF", "mild_cognitive_impairment", {"odds_ratio": 3.2}),
    ("age_over_65", "INCREASES_RISK_OF", "early_alzheimer_disease", {"odds_ratio": 4.5}),
    ("sleep_deprivation_chronic", "INCREASES_RISK_OF", "mild_cognitive_impairment", {"odds_ratio": 1.8}),
    ("sleep_deprivation_chronic", "INCREASES_RISK_OF", "major_depressive_disorder", {"odds_ratio": 2.1}),
    ("sedentary_lifestyle", "INCREASES_RISK_OF", "mild_cognitive_impairment", {"odds_ratio": 1.6}),
    ("chronic_high_stress", "INCREASES_RISK_OF", "burnout_syndrome", {"odds_ratio": 3.8}),
    ("chronic_high_stress", "INCREASES_RISK_OF", "generalized_anxiety_disorder", {"odds_ratio": 2.5}),
    ("social_isolation", "INCREASES_RISK_OF", "major_depressive_disorder", {"odds_ratio": 2.7}),
    ("social_isolation", "INCREASES_RISK_OF", "mild_cognitive_impairment", {"odds_ratio": 1.9}),
    ("family_history_dementia", "INCREASES_RISK_OF", "early_alzheimer_disease", {"odds_ratio": 3.5}),
    ("traumatic_brain_injury", "INCREASES_RISK_OF", "post_concussion_syndrome", {"odds_ratio": 5.0}),
    ("excessive_screen_time", "INCREASES_RISK_OF", "insomnia_disorder", {"odds_ratio": 1.7}),
]

EVIDENCE_SUPPORTS = [
    (
        "10.2196/86262",
        [
            ("sleep_fragmentation", "INDICATES", "fatigue"),
            ("reduced_daily_mobility", "INDICATES", "fatigue"),
            ("gait_irregularity", "INDICATES", "psychomotor_slowing"),
        ],
    ),
    (
        "10.48550/arXiv.2509.23158",
        [
            ("typing_speed_decline", "INDICATES", "psychomotor_slowing"),
            ("increased_app_switching", "INDICATES", "attention_deficit"),
            ("social_interaction_decline", "INDICATES", "social_withdrawal"),
        ],
    ),
    (
        "10.1038/s41591-025-03468-w",
        [
            ("typing_speed_decline", "INDICATES", "attention_deficit"),
            ("sleep_fragmentation", "INDICATES", "concentration_difficulty"),
        ],
    ),
    (
        "10.1038/s44400-025-00040-0",
        [
            ("voice_prosody_change", "INDICATES", "mood_changes"),
            ("word_finding_pauses", "INDICATES", "word_finding_difficulty"),
        ],
    ),
    (
        "10.1038/s43587-021-00040-w",
        [
            ("gait_irregularity", "INDICATES", "spatial_disorientation"),
            ("reduced_daily_mobility", "INDICATES", "social_withdrawal"),
        ],
    ),
    (
        "10.1177/20552076221089092",
        [
            ("screen_time_spike", "INDICATES", "sleep_disturbance"),
            ("response_time_increase", "INDICATES", "attention_deficit"),
        ],
    ),
    (
        "10.3389/fnagi.2023.1168468",
        [
            ("keystroke_rhythm_irregularity", "INDICATES", "psychomotor_slowing"),
            ("typing_error_increase", "INDICATES", "attention_deficit"),
        ],
    ),
    (
        "10.1016/j.sleep.2023.05.012",
        [
            ("circadian_rhythm_shift", "INDICATES", "sleep_disturbance"),
            ("nighttime_phone_usage", "INDICATES", "sleep_disturbance"),
        ],
    ),
    ("10.1038/s41746-023-00765-z", [("social_interaction_decline", "INDICATES", "mood_changes")]),
    (
        "10.1093/jamia/ocac042",
        [
            ("screen_time_spike", "INDICATES", "concentration_difficulty"),
            ("circadian_rhythm_shift", "INDICATES", "sleep_disturbance"),
        ],
    ),
    ("10.1111/psyp.14228", [("heart_rate_variability_decrease", "INDICATES", "fatigue")]),
    ("10.1177/10870547231162", [("increased_app_switching", "INDICATES", "restlessness")]),
]

