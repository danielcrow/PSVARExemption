# PSVAR Exemption Workflow - Visual Diagrams

## Complete System Architecture

```mermaid
graph TB
    User[Transport Operator] -->|Starts Application| IntakeAgent[Intake Agent]
    IntakeAgent -->|Invokes| DataFlow[Data Collection Flow]
    
    DataFlow -->|Step 1| Welcome[Welcome & Explain Process]
    Welcome -->|Step 2| CompanyData[Collect Company Details]
    CompanyData -->|Step 3| ServiceData[Collect Service Information]
    ServiceData -->|Step 4| ScopeCheck{In Scope?}
    
    ScopeCheck -->|No - Not HTS| OutScope1[OUT_OF_SCOPE]
    ScopeCheck -->|No - Not Closed Door| OutScope1
    ScopeCheck -->|No - No Paying Customers| OutScope1
    ScopeCheck -->|Yes| FleetData[Collect Fleet Information]
    
    FleetData -->|Step 5| VINCollection[Collect All VINs]
    VINCollection -->|Step 6| VINValidation[Validate VINs Tool]
    VINValidation -->|Invalid| VINCollection
    VINValidation -->|Valid| CertQuestion{Has Certificate?}
    
    CertQuestion -->|Yes| CertDetails[Collect Certificate Details]
    CertQuestion -->|No| Confirm
    CertDetails -->|Step 7| OpConditions[Collect Operational Conditions]
    OpConditions -->|Step 8| Confirm[Confirmation Step]
    
    Confirm -->|Not Confirmed| CompanyData
    Confirm -->|Confirmed| AssessmentFlow[Assessment Flow]
    
    AssessmentFlow -->|Step 1| EligibilityCheck[Eligibility Check]
    EligibilityCheck -->|Step 2| BandDetermination[Band Determination]
    BandDetermination -->|Step 3| MilestoneEval[Milestone Evaluation]
    MilestoneEval -->|Step 4| CertValidation[Certificate Validation]
    CertValidation -->|Step 5| OpCheck[Operational Compliance Check]
    OpCheck -->|Step 6| DecisionEngine[Decision Engine]
    
    DecisionEngine -->|Decision| FinalOutcome{Final Outcome}
    
    FinalOutcome -->|CAN_HAVE_EXEMPTION| EmailFlow[Email Notification Flow]
    FinalOutcome -->|CANNOT_HAVE_EXEMPTION| EmailFlow
    FinalOutcome -->|EXEMPTION_NOT_REQUIRED| EmailFlow
    FinalOutcome -->|OUT_OF_SCOPE| EmailFlow
    FinalOutcome -->|FURTHER_INVESTIGATION| DVSAFlow[DVSA Review Flow]
    
    DVSAFlow -->|Creates| DVSATask[DVSA Task]
    DVSATask -->|Assigns to| DVSAAgent[DVSA Officer Agent]
    DVSAAgent -->|Reviews| CaseReview[Review Case Details]
    CaseReview -->|May Use| VerifyVIN[Verify VIN with DVLA]
    CaseReview -->|May Use| RequestInfo[Request Additional Info]
    CaseReview -->|Makes| OfficerDecision[Officer Decision]
    OfficerDecision -->|Documents| Rationale[Document Rationale]
    Rationale -->|Triggers| EmailFlow
    
    EmailFlow -->|Formats| EmailBody[Format Email Body]
    EmailBody -->|Generates| Transcript[Generate Transcript]
    Transcript -->|Attaches| AttachFile[Attach Transcript File]
    AttachFile -->|Sends via| Gmail[Gmail API]
    Gmail -->|Delivers to| User
    
    OutScope1 -->|Notifies| EmailFlow
    
    style IntakeAgent fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style DVSAAgent fill:#9B59B6,stroke:#7D3C98,color:#fff
    style DataFlow fill:#50C878,stroke:#2E7D4E,color:#fff
    style AssessmentFlow fill:#50C878,stroke:#2E7D4E,color:#fff
    style DVSAFlow fill:#F39C12,stroke:#D68910,color:#fff
    style EmailFlow fill:#E74C3C,stroke:#C0392B,color:#fff
    style DecisionEngine fill:#F39C12,stroke:#D68910,color:#fff
```

---

## Data Collection Flow (Detailed)

```mermaid
flowchart TD
    Start([START]) --> Welcome[Display Welcome Message]
    Welcome --> CompanyForm[Company Details Form]
    
    CompanyForm --> CompanyFields{All Fields<br/>Complete?}
    CompanyFields -->|No| CompanyForm
    CompanyFields -->|Yes| ServiceForm[Service Information Form]
    
    ServiceForm --> ServiceFields{All Fields<br/>Complete?}
    ServiceFields -->|No| ServiceForm
    ServiceFields -->|Yes| ScopeCheck[Check Scope Eligibility]
    
    ScopeCheck --> IsHTS{Service Type<br/>= HTS?}
    IsHTS -->|No| OutScope[Return OUT_OF_SCOPE]
    IsHTS -->|Yes| IsClosedDoor{Closed Door<br/>Service?}
    
    IsClosedDoor -->|No| OutScope
    IsClosedDoor -->|Yes| HasPayingCustomers{Has Paying<br/>Customers?}
    
    HasPayingCustomers -->|No| OutScope
    HasPayingCustomers -->|Yes| FleetForm[Fleet Information Form]
    
    FleetForm --> FleetFields{All Fields<br/>Complete?}
    FleetFields -->|No| FleetForm
    FleetFields -->|Yes| FleetValidation[Validate Fleet Counts]
    
    FleetValidation --> CountsMatch{Counts Add Up<br/>to Total?}
    CountsMatch -->|No| FleetError[Show Error Message]
    FleetError --> FleetForm
    CountsMatch -->|Yes| VINForm[VIN Collection Form]
    
    VINForm --> VINCount{Correct Number<br/>of VINs?}
    VINCount -->|No| VINForm
    VINCount -->|Yes| VINValidate[Validate Each VIN]
    
    VINValidate --> VINCheck{All VINs<br/>Valid?}
    VINCheck -->|No| VINError[Show VIN Errors]
    VINError --> VINForm
    VINCheck -->|Yes| CertQuestion{Has Exemption<br/>Certificate?}
    
    CertQuestion -->|No| ConfirmForm
    CertQuestion -->|Yes| CertForm[Certificate Details Form]
    
    CertForm --> CertFields{All Fields<br/>Complete?}
    CertFields -->|No| CertForm
    CertFields -->|Yes| OpForm[Operational Conditions Form]
    
    OpForm --> OpFields{All Fields<br/>Complete?}
    OpFields -->|No| OpForm
    OpFields -->|Yes| ConfirmForm[Confirmation Form]
    
    ConfirmForm --> ReviewData[Display All Collected Data]
    ReviewData --> UserConfirm{User<br/>Confirms?}
    
    UserConfirm -->|No - Edit Company| CompanyForm
    UserConfirm -->|No - Edit Service| ServiceForm
    UserConfirm -->|No - Edit Fleet| FleetForm
    UserConfirm -->|No - Edit VINs| VINForm
    UserConfirm -->|No - Edit Certificate| CertForm
    UserConfirm -->|Yes| Output[Return Complete Application Data]
    
    Output --> End([END])
    OutScope --> End
    
    style Start fill:#2ECC71,stroke:#27AE60,color:#fff
    style End fill:#E74C3C,stroke:#C0392B,color:#fff
    style VINValidate fill:#F39C12,stroke:#D68910,color:#fff
    style FleetValidation fill:#F39C12,stroke:#D68910,color:#fff
    style ScopeCheck fill:#F39C12,stroke:#D68910,color:#fff
```

---

## Assessment Flow (Detailed)

```mermaid
flowchart TD
    Start([START]) --> Input[Receive Application Data]
    Input --> Step1[Step 1: Eligibility Screening]
    
    Step1 --> CheckHTS{Service Type<br/>= HTS?}
    CheckHTS -->|No| OutScope[Decision: OUT_OF_SCOPE]
    CheckHTS -->|Yes| CheckClosedDoor{Closed Door?}
    
    CheckClosedDoor -->|No| OutScope
    CheckClosedDoor -->|Yes| CheckPaying{Paying<br/>Customers?}
    
    CheckPaying -->|No| OutScope
    CheckPaying -->|Yes| Step2[Step 2: Fleet Assessment]
    
    Step2 --> CheckFleetSize{Fleet Size<br/>> 0?}
    CheckFleetSize -->|No| OutScope
    CheckFleetSize -->|Yes| CheckCompliance{All Vehicles<br/>Fully Compliant?}
    
    CheckCompliance -->|Yes| NotNeeded[Decision: EXEMPTION_NOT_REQUIRED]
    CheckCompliance -->|No| Step3[Step 3: Band Determination]
    
    Step3 --> DetermineBand[Calculate Band from Fleet Size]
    DetermineBand --> BandResult{Band}
    
    BandResult -->|1-5 vehicles| BandA[Band A]
    BandResult -->|6-9 vehicles| BandB[Band B]
    BandResult -->|10-29 vehicles| BandC[Band C]
    BandResult -->|30+ vehicles| BandD[Band D]
    
    BandA --> Step4
    BandB --> Step4
    BandC --> Step4
    BandD --> Step4[Step 4: Milestone Evaluation]
    
    Step4 --> GetDate[Get Assessment Date]
    GetDate --> CheckDate{Date After<br/>2026-07-31?}
    
    CheckDate -->|Yes| Expired[Decision: CANNOT_HAVE_EXEMPTION<br/>Regime Expired]
    CheckDate -->|No| CalcRequirements[Calculate Required Counts<br/>for Band and Date]
    
    CalcRequirements --> CheckFully{Meets Fully<br/>Compliant<br/>Requirement?}
    CheckFully -->|No| MilestoneFail[Milestone Non-Compliant]
    CheckFully -->|Yes| CheckPartial{Meets Partially<br/>Compliant<br/>Requirement?}
    
    CheckPartial -->|No| MilestoneFail
    CheckPartial -->|Yes| CheckRemaining{Remaining Must Be<br/>Partially Compliant?}
    
    CheckRemaining -->|Yes, but has non-compliant| MilestoneFail
    CheckRemaining -->|No or all compliant| MilestonePass[Milestone Compliant]
    
    MilestoneFail --> Step5
    MilestonePass --> Step5[Step 5: Certificate Validation]
    
    Step5 --> HasCert{Has<br/>Certificate?}
    
    HasCert -->|No| NoCertMilestone{Milestone<br/>Compliant?}
    NoCertMilestone -->|No| CannotHave[Decision: CANNOT_HAVE_EXEMPTION]
    NoCertMilestone -->|Yes| CanApply[Decision: CAN_HAVE_EXEMPTION<br/>Can Apply for Certificate]
    
    HasCert -->|Yes| CheckCertDates[Check Certificate Dates]
    CheckCertDates --> CertExpired{Certificate<br/>Expired?}
    
    CertExpired -->|Yes| CannotHave
    CertExpired -->|No| ValidCert[Valid Certificate]
    
    ValidCert --> Step6[Step 6: Operational Compliance]
    
    Step6 --> CheckOnboard{Copy Carried<br/>Onboard?}
    CheckOnboard -->|No| OpFail[Operational Non-Compliant]
    CheckOnboard -->|Yes| CheckAltTransport{Alternative<br/>Transport<br/>Available?}
    
    CheckAltTransport -->|No| OpFail
    CheckAltTransport -->|Yes| CheckWritten{Written<br/>Confirmation<br/>Retained?}
    
    CheckWritten -->|No| OpFail
    CheckWritten -->|Yes| CheckRead{Read Band<br/>Requirements?}
    
    CheckRead -->|No| OpFail
    CheckRead -->|Yes| CheckFleetChange{Fleet Size<br/>Changed?}
    
    CheckFleetChange -->|No| OpPass[Operational Compliant]
    CheckFleetChange -->|Yes| CheckNotified{DfT Notified<br/>Within 5 Days?}
    
    CheckNotified -->|No| OpFail
    CheckNotified -->|Yes| OpPass
    
    OpFail --> Step7
    OpPass --> Step7[Step 7: Final Decision]
    
    Step7 --> FinalCheck{Milestone AND<br/>Operational<br/>Compliant?}
    
    FinalCheck -->|No| CheckMissing{Missing<br/>Information?}
    CheckMissing -->|Yes| FurtherInv[Decision: FURTHER_INVESTIGATION_REQUIRED]
    CheckMissing -->|No| CannotHave
    
    FinalCheck -->|Yes| CheckMissingFinal{Missing<br/>Information?}
    CheckMissingFinal -->|Yes| FurtherInv
    CheckMissingFinal -->|No| CanHave[Decision: CAN_HAVE_EXEMPTION]
    
    OutScope --> PrepareOutput
    NotNeeded --> PrepareOutput
    CannotHave --> PrepareOutput
    CanApply --> PrepareOutput
    CanHave --> PrepareOutput
    Expired --> PrepareOutput
    FurtherInv --> CreateTask[Create DVSA Task]
    
    CreateTask --> PrepareOutput[Prepare Output Payload]
    PrepareOutput --> Output[Return Assessment Output]
    Output --> End([END])
    
    style Start fill:#2ECC71,stroke:#27AE60,color:#fff
    style End fill:#E74C3C,stroke:#C0392B,color:#fff
    style Step1 fill:#3498DB,stroke:#2980B9,color:#fff
    style Step2 fill:#3498DB,stroke:#2980B9,color:#fff
    style Step3 fill:#3498DB,stroke:#2980B9,color:#fff
    style Step4 fill:#3498DB,stroke:#2980B9,color:#fff
    style Step5 fill:#3498DB,stroke:#2980B9,color:#fff
    style Step6 fill:#3498DB,stroke:#2980B9,color:#fff
    style Step7 fill:#3498DB,stroke:#2980B9,color:#fff
    style FurtherInv fill:#F39C12,stroke:#D68910,color:#fff
    style CreateTask fill:#F39C12,stroke:#D68910,color:#fff
```

---

## DVSA Officer Review Flow (Detailed)

```mermaid
flowchart TD
    Start([START]) --> Receive[Receive Case for Review]
    Receive --> Load[Load Case Details]
    
    Load --> Display[Display Case Information]
    Display --> ShowRationale[Show Rationale for Review]
    ShowRationale --> ShowMissing[Show Missing Information]
    ShowMissing --> ShowData[Show All Collected Data]
    
    ShowData --> OfficerMenu{Officer Action}
    
    OfficerMenu -->|Review Details| ReviewMore[Review Additional Details]
    ReviewMore --> OfficerMenu
    
    OfficerMenu -->|Verify VIN| SelectVIN[Select VIN to Verify]
    SelectVIN --> CallDVLA[Call DVLA API]
    CallDVLA --> DVLAResult{VIN Found?}
    
    DVLAResult -->|Yes| ShowVehicle[Display Vehicle Details]
    DVLAResult -->|No| ShowNotFound[VIN Not Found in DVLA]
    
    ShowVehicle --> UpdateNotes[Update Case Notes]
    ShowNotFound --> UpdateNotes
    UpdateNotes --> OfficerMenu
    
    OfficerMenu -->|Request Info| ComposeRequest[Compose Information Request]
    ComposeRequest --> SendRequest[Send Email to Operator]
    SendRequest --> WaitResponse[Wait for Response]
    WaitResponse --> ResponseReceived{Response<br/>Received?}
    
    ResponseReceived -->|Yes| UpdateCase[Update Case with New Info]
    ResponseReceived -->|Timeout| EscalateCase[Escalate Case]
    
    UpdateCase --> OfficerMenu
    EscalateCase --> OfficerMenu
    
    OfficerMenu -->|Make Decision| ConfirmReady{All Information<br/>Available?}
    
    ConfirmReady -->|No| NeedMore[Indicate What's Still Needed]
    NeedMore --> OfficerMenu
    
    ConfirmReady -->|Yes| DecisionForm[Decision Form]
    DecisionForm --> SelectDecision{Decision}
    
    SelectDecision -->|APPROVE| ApproveForm[Approve Exemption Form]
    SelectDecision -->|DENY| DenyForm[Deny Exemption Form]
    
    ApproveForm --> DocumentApprove[Document Approval Rationale]
    DenyForm --> DocumentDeny[Document Denial Rationale]
    
    DocumentApprove --> ReviewDecision[Review Decision Summary]
    DocumentDeny --> ReviewDecision
    
    ReviewDecision --> ConfirmDecision{Confirm<br/>Decision?}
    
    ConfirmDecision -->|No| DecisionForm
    ConfirmDecision -->|Yes| SaveDecision[Save Decision to Case]
    
    SaveDecision --> PrepareEmail[Prepare Outcome Email]
    PrepareEmail --> SendEmail[Send Email to Operator]
    SendEmail --> CloseCase[Close Case]
    CloseCase --> LogDecision[Log Decision in System]
    LogDecision --> End([END])
    
    style Start fill:#2ECC71,stroke:#27AE60,color:#fff
    style End fill:#E74C3C,stroke:#C0392B,color:#fff
    style DecisionForm fill:#9B59B6,stroke:#7D3C98,color:#fff
    style ApproveForm fill:#2ECC71,stroke:#27AE60,color:#fff
    style DenyForm fill:#E74C3C,stroke:#C0392B,color:#fff
    style CallDVLA fill:#F39C12,stroke:#D68910,color:#fff
    style SendEmail fill:#3498DB,stroke:#2980B9,color:#fff
```

---

## Email Notification Flow (Detailed)

```mermaid
flowchart TD
    Start([START]) --> Input[Receive Email Payload]
    Input --> CheckRecipient{Recipient<br/>Email Valid?}
    
    CheckRecipient -->|No| NoEmail[Skip Email Sending]
    CheckRecipient -->|Yes| FormatSubject[Format Email Subject]
    
    FormatSubject --> OutcomeType{Outcome Type}
    
    OutcomeType -->|CAN_HAVE_EXEMPTION| SubjectApprove[Subject: Eligible]
    OutcomeType -->|CANNOT_HAVE_EXEMPTION| SubjectDeny[Subject: Not Eligible]
    OutcomeType -->|FURTHER_INVESTIGATION| SubjectReview[Subject: Under Review]
    OutcomeType -->|OUT_OF_SCOPE| SubjectScope[Subject: Out of Scope]
    OutcomeType -->|EXEMPTION_NOT_REQUIRED| SubjectNotNeeded[Subject: Not Required]
    
    SubjectApprove --> FormatBody
    SubjectDeny --> FormatBody
    SubjectReview --> FormatBody
    SubjectScope --> FormatBody
    SubjectNotNeeded --> FormatBody[Format Email Body]
    
    FormatBody --> AddGreeting[Add Greeting]
    AddGreeting --> AddOutcome[Add Outcome Statement]
    AddOutcome --> AddRationale[Add Rationale Section]
    AddRationale --> AddNextActions[Add Next Actions Section]
    AddNextActions --> AddClosing[Add Closing]
    
    AddClosing --> GenerateTranscript[Generate Conversation Transcript]
    GenerateTranscript --> FormatTranscript[Format as Text File]
    FormatTranscript --> AttachFile[Attach Transcript to Email]
    
    AttachFile --> ConnectGmail[Connect to Gmail API]
    ConnectGmail --> AuthCheck{OAuth2<br/>Authenticated?}
    
    AuthCheck -->|No| AuthError[Authentication Error]
    AuthCheck -->|Yes| ComposeMessage[Compose MIME Message]
    
    ComposeMessage --> EncodeMessage[Base64 Encode Message]
    EncodeMessage --> SendAttempt[Attempt to Send]
    
    SendAttempt --> SendResult{Send<br/>Successful?}
    
    SendResult -->|Yes| LogSuccess[Log Successful Delivery]
    SendResult -->|No| CheckRetry{Retry<br/>Attempts<br/>< 3?}
    
    CheckRetry -->|Yes| WaitRetry[Wait 5 Seconds]
    WaitRetry --> SendAttempt
    
    CheckRetry -->|No| LogFailure[Log Delivery Failure]
    
    LogSuccess --> ReturnSuccess[Return Success Response]
    LogFailure --> ReturnFailure[Return Failure Response]
    AuthError --> ReturnFailure
    NoEmail --> ReturnSkipped[Return Skipped Response]
    
    ReturnSuccess --> End([END])
    ReturnFailure --> End
    ReturnSkipped --> End
    
    style Start fill:#2ECC71,stroke:#27AE60,color:#fff
    style End fill:#E74C3C,stroke:#C0392B,color:#fff
    style ConnectGmail fill:#9B59B6,stroke:#7D3C98,color:#fff
    style SendAttempt fill:#F39C12,stroke:#D68910,color:#fff
    style LogSuccess fill:#2ECC71,stroke:#27AE60,color:#fff
    style LogFailure fill:#E74C3C,stroke:#C0392B,color:#fff
```

---

## Decision Outcomes Summary

```mermaid
graph LR
    Assessment[Assessment Complete] --> Decision{Final Decision}
    
    Decision -->|All Compliant| NotRequired[EXEMPTION_NOT_REQUIRED]
    Decision -->|Not HTS/Closed-Door/Paying| OutScope[OUT_OF_SCOPE]
    Decision -->|No Cert + Meets Milestones| CanApply[CAN_HAVE_EXEMPTION<br/>Can Apply]
    Decision -->|No Cert + Fails Milestones| Cannot[CANNOT_HAVE_EXEMPTION]
    Decision -->|Valid Cert + All Compliant| CanUse[CAN_HAVE_EXEMPTION<br/>Can Use]
    Decision -->|Expired Cert| Cannot
    Decision -->|Valid Cert + Non-Compliant| Review[FURTHER_INVESTIGATION_REQUIRED]
    Decision -->|Missing Information| Review
    
    NotRequired --> Email[Email Notification]
    OutScope --> Email
    CanApply --> Email
    Cannot --> Email
    CanUse --> Email
    Review --> DVSATask[DVSA Officer Task]
    
    DVSATask --> OfficerReview[Officer Reviews]
    OfficerReview --> OfficerDecision{Officer Decision}
    
    OfficerDecision -->|Approve| Email
    OfficerDecision -->|Deny| Email
    
    Email --> Operator[Operator Receives Email]
    
    style NotRequired fill:#2ECC71,stroke:#27AE60,color:#fff
    style OutScope fill:#95A5A6,stroke:#7F8C8D,color:#fff
    style CanApply fill:#3498DB,stroke:#2980B9,color:#fff
    style CanUse fill:#2ECC71,stroke:#27AE60,color:#fff
    style Cannot fill:#E74C3C,stroke:#C0392B,color:#fff
    style Review fill:#F39C12,stroke:#D68910,color:#fff
    style DVSATask fill:#9B59B6,stroke:#7D3C98,color:#fff
```

---

## Component Interaction Diagram

```mermaid
sequenceDiagram
    participant Operator
    participant IntakeAgent
    participant DataFlow
    participant VINTool
    participant AssessmentFlow
    participant DecisionTool
    participant DVSAAgent
    participant EmailFlow
    participant Gmail
    
    Operator->>IntakeAgent: Start application
    IntakeAgent->>DataFlow: Invoke data collection
    
    loop Data Collection
        DataFlow->>Operator: Request information
        Operator->>DataFlow: Provide information
        DataFlow->>VINTool: Validate VINs
        VINTool-->>DataFlow: Validation result
    end
    
    DataFlow->>Operator: Confirm all data
    Operator->>DataFlow: Confirmed
    DataFlow-->>IntakeAgent: Complete application data
    
    IntakeAgent->>AssessmentFlow: Invoke assessment
    AssessmentFlow->>DecisionTool: Evaluate eligibility
    DecisionTool-->>AssessmentFlow: Assessment result
    AssessmentFlow-->>IntakeAgent: Assessment outcome
    
    alt Further Investigation Required
        IntakeAgent->>DVSAAgent: Create review task
        DVSAAgent->>Operator: Request additional info
        Operator->>DVSAAgent: Provide info
        DVSAAgent->>DecisionTool: Make final decision
        DecisionTool-->>DVSAAgent: Final outcome
        DVSAAgent->>EmailFlow: Send outcome email
    else Direct Decision
        IntakeAgent->>EmailFlow: Send outcome email
    end
    
    EmailFlow->>Gmail: Send email with attachment
    Gmail-->>Operator: Deliver email
    EmailFlow-->>IntakeAgent: Email sent confirmation
    IntakeAgent->>Operator: Display outcome and next steps
```

---

## Timeline Gantt Chart

```mermaid
gantt
    title PSVAR Implementation Timeline (10 Weeks)
    dateFormat YYYY-MM-DD
    section Phase 1: Foundation
    Core Infrastructure           :p1a, 2026-06-02, 7d
    Python Tools                  :p1b, 2026-06-02, 7d
    Basic Assessment Flow         :p1c, 2026-06-09, 7d
    Unit Tests                    :p1d, 2026-06-09, 7d
    
    section Phase 2: Data Collection
    Design Data Flow              :p2a, 2026-06-16, 7d
    Implement User Activities     :p2b, 2026-06-16, 7d
    VIN Validation Integration    :p2c, 2026-06-23, 7d
    E2E Testing                   :p2d, 2026-06-23, 7d
    
    section Phase 3: DVSA Workflow
    DVSA Task Creator             :p3a, 2026-06-30, 7d
    DVSA Review Flow              :p3b, 2026-06-30, 7d
    DVSA Officer Agent            :p3c, 2026-07-07, 7d
    Officer Testing               :p3d, 2026-07-07, 7d
    
    section Phase 4: Email
    Email Notification Flow       :p4a, 2026-07-14, 7d
    Email Templates               :p4b, 2026-07-14, 7d
    
    section Phase 5: Testing
    Comprehensive Testing         :p5a, 2026-07-21, 14d
    Bug Fixes                     :p5b, 2026-07-21, 14d
    
    section Phase 6: Deployment
    Production Deployment         :p6a, 2026-08-04, 7d
    User Training                 :p6b, 2026-08-04, 7d
```

---

*All diagrams are in Mermaid format and can be rendered in any Mermaid-compatible viewer or documentation system.*