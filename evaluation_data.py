evaluation_cases = [

    # ==================================================
    # NORMAL
    # ==================================================

    {
        "question": "How many unused annual leave days can I carry forward?",
        "expected_policy": "HR001",
        "expected_sufficiency": "SUFFICIENT",
        "category": "normal"
    },

    {
        "question": "Do I need a medical certificate after three days of sick leave?",
        "expected_policy": "HR002",
        "expected_sufficiency": "SUFFICIENT",
        "category": "normal"
    },

    {
        "question": "What is the company's work-from-home policy?",
        "expected_policy": "HR003",
        "expected_sufficiency": "SUFFICIENT",
        "category": "normal"
    },

    {
        "question": "What does the parental leave policy provide?",
        "expected_policy": "HR004",
        "expected_sufficiency": "SUFFICIENT",
        "category": "normal"
    },

    {
        "question": "What is the company's expense reimbursement policy?",
        "expected_policy": "HR005",
        "expected_sufficiency": "SUFFICIENT",
        "category": "normal"
    },


    # ==================================================
    # PARAPHRASE
    # ==================================================

    {
        "question": "What happens to my leftover holidays at the end of the year?",
        "expected_policy": "HR001",
        "expected_sufficiency": "SUFFICIENT",
        "category": "paraphrase"
    },

    {
        "question": "When do I need to provide a doctor's certificate for sick leave?",
        "expected_policy": "HR002",
        "expected_sufficiency": "SUFFICIENT",
        "category": "paraphrase"
    },

    {
        "question": "Am I allowed to work remotely?",
        "expected_policy": "HR003",
        "expected_sufficiency": "SUFFICIENT",
        "category": "paraphrase"
    },

    {
        "question": "How much paid parental leave can an employee take?",
        "expected_policy": "HR004",
        "expected_sufficiency": "SUFFICIENT",
        "category": "paraphrase"
    },

    {
        "question": "How do I claim reimbursement for a work expense?",
        "expected_policy": "HR005",
        "expected_sufficiency": "SUFFICIENT",
        "category": "paraphrase"
    },


    # ==================================================
    # INSUFFICIENT
    # ==================================================

    {
        "question": "Can I carry forward sick leave into next year?",
        "expected_policy": "HR002",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "insufficient"
    },

    {
        "question": "Can I work from another country while on vacation?",
        "expected_policy": "HR003",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "insufficient"
    },

    {
        "question": "Can grandparents take parental leave under this policy?",
        "expected_policy": "HR004",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "insufficient"
    },

    {
        "question": "Can the company reimburse my personal vacation expenses?",
        "expected_policy": "HR005",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "insufficient"
    },


    # ==================================================
    # OUT OF SCOPE
    # ==================================================

    {
        "question": "How many public holidays are there this year?",
        "expected_policy": None,
        "expected_sufficiency": "INSUFFICIENT",
        "category": "out_of_scope"
    },

    {
        "question": "What is the company's health insurance coverage?",
        "expected_policy": None,
        "expected_sufficiency": "INSUFFICIENT",
        "category": "out_of_scope"
    },

    {
        "question": "What is the employee dress code?",
        "expected_policy": None,
        "expected_sufficiency": "INSUFFICIENT",
        "category": "out_of_scope"
    },

    {
        "question": "When will employees receive their annual salary increment?",
        "expected_policy": None,
        "expected_sufficiency": "INSUFFICIENT",
        "category": "out_of_scope"
    },

    {
        "question": "Does the company provide free meals to employees?",
        "expected_policy": None,
        "expected_sufficiency": "INSUFFICIENT",
        "category": "out_of_scope"
    },


    # ==================================================
    # CONFLICTING CUE — INSUFFICIENT
    #
    # Correct topical policy exists, but that policy
    # does NOT contain enough information to answer.
    # ==================================================

    {
        "question": "Do unused sick leave days carry forward like annual leave?",
        "expected_policy": "HR002",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "conflicting_cue_insufficient"
    },

    {
        "question": "Do I need manager approval to take sick leave?",
        "expected_policy": "HR002",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "conflicting_cue_insufficient"
    },

    {
        "question": "Can annual leave be taken while working remotely?",
        "expected_policy": "HR001",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "conflicting_cue_insufficient"
    },

    {
        "question": "Can parental leave be carried forward to the next year?",
        "expected_policy": "HR004",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "conflicting_cue_insufficient"
    },


    # ==================================================
    # IRRELEVANT CROSS-POLICY BACKGROUND
    #
    # Another policy concept appears in the question,
    # but it does NOT materially affect the requested
    # answer.
    #
    # Expected: SUFFICIENT
    # ==================================================

    {
        "question": "I work remotely. Within how many days must I submit a business expense claim?",
        "expected_policy": "HR005",
        "expected_sufficiency": "SUFFICIENT",
        "category": "irrelevant_background"
    },

    {
        "question": "I currently work remotely. How many weeks of paid parental leave are eligible employees entitled to?",
        "expected_policy": "HR004",
        "expected_sufficiency": "SUFFICIENT",
        "category": "irrelevant_background"
    },


    # ==================================================
    # SUPPORTED MATERIAL CONDITION
    #
    # The condition matters to the answer AND the
    # retrieved policy explicitly addresses it.
    #
    # Expected: SUFFICIENT
    # ==================================================

    {
        "question": "Can a new employee on probation work remotely?",
        "expected_policy": "HR003",
        "expected_sufficiency": "SUFFICIENT",
        "category": "material_condition_supported"
    },


    # ==================================================
    # UNSUPPORTED MATERIAL CONDITION
    #
    # The policy covers the general topic, but the
    # additional condition is not addressed.
    #
    # Expected: INSUFFICIENT
    # ==================================================

    {
        "question": "Can I work remotely from another country?",
        "expected_policy": "HR003",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "material_condition_unsupported"
    },

    {
        "question": "If I have unused annual leave, can I work remotely two days per week with manager approval?",
        "expected_policy": "HR003",
        "expected_sufficiency": "INSUFFICIENT",
        "category": "material_condition_unsupported"
    },


    # ==================================================
    # CONDITIONAL
    # ==================================================

    {
        "question": "Can employees work from home two days a week?",
        "expected_policy": "HR003",
        "expected_sufficiency": "SUFFICIENT",
        "category": "conditional"
    },

    {
        "question": "Can I work remotely if my manager approves it?",
        "expected_policy": "HR003",
        "expected_sufficiency": "SUFFICIENT",
        "category": "conditional"
    },

    {
        "question": "If I have been sick for three consecutive working days, do I need a medical certificate?",
        "expected_policy": "HR002",
        "expected_sufficiency": "SUFFICIENT",
        "category": "conditional"
    }
]
