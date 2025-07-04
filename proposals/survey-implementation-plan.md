# Survey Implementation Plan for Existing Pairwise Voting System

## Current State Analysis

You have:
- ✅ Pairwise voting system
- ✅ Database and APIs
- ✅ User management
- ✅ Referral system
- ❌ Complex survey structure support
- ❌ Multiple question types
- ❌ Survey sections and flow control

## Implementation Strategy

### Phase 1: Database Schema Extensions

**New Tables Needed:**

```sql
-- Survey definitions
CREATE TABLE surveys (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  version VARCHAR(50) DEFAULT '1.0',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Survey sections
CREATE TABLE survey_sections (
  id SERIAL PRIMARY KEY,
  survey_id INTEGER REFERENCES surveys(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  order_index INTEGER NOT NULL,
  is_required BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Survey questions
CREATE TABLE survey_questions (
  id SERIAL PRIMARY KEY,
  section_id INTEGER REFERENCES survey_sections(id),
  question_text TEXT NOT NULL,
  question_type VARCHAR(50) NOT NULL, -- 'multiple_choice', 'slider', 'text', 'pairwise', 'ranking'
  options JSONB, -- For multiple choice, ranking options
  min_value INTEGER, -- For sliders
  max_value INTEGER, -- For sliders
  default_value INTEGER, -- For sliders
  order_index INTEGER NOT NULL,
  is_required BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Survey responses (extends existing)
CREATE TABLE survey_responses (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  survey_id INTEGER REFERENCES surveys(id),
  section_id INTEGER REFERENCES survey_sections(id),
  question_id INTEGER REFERENCES survey_questions(id),
  answer_value TEXT, -- For text, multiple choice
  answer_numeric INTEGER, -- For sliders, rankings
  answer_json JSONB, -- For complex answers like pairwise allocations
  created_at TIMESTAMP DEFAULT NOW()
);

-- Survey progress tracking
CREATE TABLE survey_progress (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  survey_id INTEGER REFERENCES surveys(id),
  current_section_id INTEGER REFERENCES survey_sections(id),
  current_question_id INTEGER REFERENCES survey_questions(id),
  is_completed BOOLEAN DEFAULT false,
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  UNIQUE(user_id, survey_id)
);
```

### Phase 2: API Endpoints

**New Endpoints:**

```typescript
// Survey Management
GET /api/surveys - List available surveys
GET /api/surveys/:id - Get survey details with sections and questions
GET /api/surveys/:id/sections - Get survey sections
GET /api/surveys/:id/sections/:sectionId/questions - Get questions for section

// Survey Progress
GET /api/user/:userId/surveys/:surveyId/progress - Get user's progress
POST /api/user/:userId/surveys/:surveyId/progress - Update progress
POST /api/user/:userId/surveys/:surveyId/complete - Mark survey complete

// Survey Responses
POST /api/surveys/:surveyId/responses - Submit single question response
POST /api/surveys/:surveyId/responses/batch - Submit multiple responses
GET /api/surveys/:surveyId/responses/:userId - Get user's responses

// Analytics
GET /api/surveys/:surveyId/analytics - Get survey analytics
GET /api/surveys/:surveyId/analytics/pairwise - Get pairwise voting results
GET /api/surveys/:surveyId/analytics/demographics - Get demographic breakdown
```

### Phase 3: Frontend Components

**React Components Needed:**

```typescript
// Survey Components
<SurveyContainer surveyId={id} />
<SurveySection section={section} onComplete={handleSectionComplete} />
<SurveyQuestion question={question} onAnswer={handleAnswer} />

// Question Type Components
<MultipleChoiceQuestion options={options} onSelect={handleSelect} />
<SliderQuestion min={min} max={max} defaultValue={default} onChange={handleChange} />
<TextQuestion placeholder={placeholder} onChange={handleChange} />
<PairwiseQuestion items={items} onAllocate={handleAllocate} />
<RankingQuestion items={items} onRank={handleRank} />

// Progress Components
<SurveyProgress current={current} total={total} />
<SurveyNavigation onNext={handleNext} onPrevious={handlePrevious} />
```

### Phase 4: Survey Configuration

**Survey Definition (JSON):**

```json
{
  "id": "dfda-public-opinion-2024",
  "title": "Public Opinion Survey: Reforming Medical Research",
  "description": "A survey to gauge public support for the dFDA initiative...",
  "sections": [
    {
      "id": "priorities-funding",
      "title": "Priorities and Funding",
      "questions": [
        {
          "id": "budget-allocation",
          "type": "pairwise",
          "text": "If you had $100 in tax dollars to allocate...",
          "items": [
            {"id": "military", "label": "Military Defense"},
            {"id": "medical", "label": "Medical Research"}
          ]
        },
        {
          "id": "international-cooperation",
          "type": "multiple_choice",
          "text": "If all other major nations also agreed...",
          "options": ["0%", "1%", "2-5%", "6-10%", "More than 10%", "Unsure"]
        }
      ]
    },
    {
      "id": "funding-initiative",
      "title": "Funding the Initiative for Reform",
      "questions": [
        {
          "id": "victory-bonds",
          "type": "multiple_choice",
          "text": "Would you be interested in purchasing such a bond?",
          "options": [
            "Yes, definitely",
            "Yes, probably", 
            "No, I am not interested in a bond, but I might donate.",
            "Unsure / Need more information"
          ]
        }
      ]
    }
  ]
}
```

### Phase 5: Integration with Existing System

**Modifications to Existing Code:**

1. **Extend Pairwise Component:**
```typescript
// Enhance existing pairwise component to handle survey context
interface PairwiseQuestionProps {
  items: Array<{id: string, label: string}>;
  onAllocate: (allocations: Record<string, number>) => void;
  surveyContext?: {
    surveyId: string;
    questionId: string;
    sectionId: string;
  };
}
```

2. **Add Survey Progress to User Dashboard:**
```typescript
// Add to existing user dashboard
interface UserDashboard {
  // ... existing fields
  surveyProgress: Array<{
    surveyId: string;
    surveyTitle: string;
    progress: number; // 0-100
    isCompleted: boolean;
    lastActivity: Date;
  }>;
}
```

3. **Extend Points System:**
```typescript
// Add survey completion to points system
const SURVEY_POINTS = {
  COMPLETE_SECTION: 10,
  COMPLETE_SURVEY: 50,
  SHARE_RESULTS: 25
};
```

### Phase 6: PLG Integration

**Data Export for PLG:**

```typescript
// API endpoint for PLG data sync
POST /api/plg/sync/survey/:surveyId
{
  "responses": [
    {
      "questionId": "budget-allocation",
      "answers": [
        {
          "userId": "anonymous_123",
          "demographics": {
            "age": "30-44",
            "country": "US",
            "zipCode": "12345",
            "politicalOutlook": "Centrist"
          },
          "allocations": {
            "military": 30,
            "medical": 70
          }
        }
      ]
    }
  ]
}
```

### Phase 7: Implementation Steps

1. **Week 1: Database Schema**
   - Create new tables
   - Migrate existing pairwise data
   - Add indexes for performance

2. **Week 2: API Development**
   - Implement survey management endpoints
   - Add progress tracking
   - Create response submission endpoints

3. **Week 3: Frontend Components**
   - Build survey container and navigation
   - Create question type components
   - Integrate with existing UI

4. **Week 4: Survey Configuration**
   - Convert survey.md to JSON configuration
   - Test all question types
   - Add validation and error handling

5. **Week 5: Integration & Testing**
   - Connect with existing user system
   - Add points and referral integration
   - Test PLG data export

6. **Week 6: Polish & Launch**
   - UI/UX improvements
   - Performance optimization
   - Launch and monitor

### Phase 8: Advanced Features (Future)

- **Survey Versioning**: Track changes to surveys over time
- **Conditional Logic**: Show/hide questions based on previous answers
- **A/B Testing**: Test different question formulations
- **Real-time Analytics**: Live dashboard of survey responses
- **Export Tools**: CSV/JSON export for analysis
- **Multi-language Support**: Internationalization

## Key Benefits

1. **Reuses Existing Infrastructure**: Leverages your current pairwise voting system
2. **Modular Design**: Easy to add new question types
3. **Scalable**: Can handle complex surveys with many sections
4. **PLG Ready**: Built-in data export for sentiment analysis
5. **User Friendly**: Progress tracking and resume capability
6. **Analytics Ready**: Structured data for analysis and visualization

This plan allows you to implement the comprehensive survey from survey.md while building on your existing system rather than starting from scratch. 