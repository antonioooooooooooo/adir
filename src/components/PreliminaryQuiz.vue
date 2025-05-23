<template>
  <div class="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
    <div v-if="!quizStarted && !quizCompleted">
      <h2 class="text-2xl font-bold mb-4">בחינת רמה ראשונית</h2>
      <p class="text-gray-600 mb-6">
        בחינה זו תעזור לנו להתאים את רמת השאלות עבורך. הבחינה כוללת מספר שאלות בכל נושא.
        אתה יכול לדלג על הבחינה ולחזור אליה מאוחר יותר.
      </p>
      <div class="flex gap-4">
        <button
          @click="startQuiz"
          class="flex-1 py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          התחל בחינה
        </button>
        <button
          @click="skipQuiz"
          class="flex-1 py-2 px-4 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
        >
          דלג לשלב הבא
        </button>
      </div>
    </div>

    <div v-if="quizStarted && !quizCompleted">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">שאלה {{ currentQuestionIndex + 1 }} מתוך {{ questions.length }}</h2>
        <div class="text-sm text-gray-600">
          נושא: {{ questions[currentQuestionIndex].topic }}
        </div>
      </div>

      <div class="mb-6">
        <div class="bg-gray-50 p-4 rounded-md mb-4">
          {{ questions[currentQuestionIndex].question }}
        </div>

        <div class="space-y-3">
          <button
            v-for="(answer, index) in questions[currentQuestionIndex].answers"
            :key="index"
            @click="selectAnswer(index)"
            :class="[
              'w-full text-right p-3 rounded-md transition-colors',
              selectedAnswer === index
                ? 'bg-blue-100 border-2 border-blue-500'
                : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
            ]"
          >
            {{ answer }}
          </button>
        </div>
      </div>

      <div class="flex justify-between">
        <button
          v-if="currentQuestionIndex > 0"
          @click="previousQuestion"
          class="py-2 px-4 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
        >
          שאלה קודמת
        </button>
        <button
          v-if="currentQuestionIndex < questions.length - 1"
          @click="nextQuestion"
          :disabled="selectedAnswer === null"
          :class="[
            'py-2 px-4 rounded-md ml-auto',
            selectedAnswer === null
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          ]"
        >
          שאלה הבאה
        </button>
        <button
          v-else
          @click="finishQuiz"
          :disabled="selectedAnswer === null"
          :class="[
            'py-2 px-4 rounded-md ml-auto',
            selectedAnswer === null
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-green-600 text-white hover:bg-green-700'
          ]"
        >
          סיים בחינה
        </button>
      </div>
    </div>

    <div v-if="quizCompleted">
      <h2 class="text-2xl font-bold mb-4">סיימת את בחינת הרמה!</h2>
      <p class="text-gray-600 mb-6">
        תודה על השלמת הבחינה. התוצאות שלך יעזרו לנו להתאים את רמת השאלות עבורך.
      </p>
      <div class="mb-6">
        <h3 class="font-semibold mb-2">תוצאות לפי נושא:</h3>
        <div class="space-y-2">
          <div
            v-for="(score, topic) in topicScores"
            :key="topic"
            class="flex justify-between p-2 bg-gray-50 rounded"
          >
            <span>{{ topic }}</span>
            <span class="font-medium">{{ Math.round(score * 100) }}%</span>
          </div>
        </div>
      </div>
      <button
        @click="goToMainPage"
        class="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700"
      >
        המשך לתרגול
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PreliminaryQuiz',
  data() {
    return {
      quizStarted: false,
      quizCompleted: false,
      currentQuestionIndex: 0,
      selectedAnswer: null,
      userAnswers: [],
      questions: [
        {
          topic: 'בעיות תנועה',
          question: 'שתי מכוניות יוצאות זו לקראת זו מערים A ו-B המרוחקות 200 ק"מ זו מזו. המכונית הראשונה נוסעת במהירות של 60 קמ"ש והשנייה במהירות של 40 קמ"ש. כעבור כמה שעות ייפגשו המכוניות?',
          answers: [
            '2 שעות',
            '1.5 שעות',
            '2.5 שעות',
            '3 שעות'
          ],
          correctAnswer: 1
        },
        {
          topic: 'סדרות',
          question: 'בסדרה חשבונית, האיבר הראשון הוא 3 וההפרש הוא 4. מה האיבר העשירי בסדרה?',
          answers: [
            '39',
            '40',
            '36',
            '43'
          ],
          correctAnswer: 0
        },
        {
          topic: 'הסתברות',
          question: 'בכד יש 3 כדורים אדומים ו-2 כדורים כחולים. מה ההסתברות להוציא כדור אדום?',
          answers: [
            '2/5',
            '3/5',
            '1/2',
            '3/2'
          ],
          correctAnswer: 1
        },
        {
          topic: 'גיאומטריה',
          question: 'במשולש ישר זווית, אחד הניצבים הוא 3 והיתר הוא 5. מה אורך הניצב השני?',
          answers: [
            '4',
            '3',
            '5',
            '6'
          ],
          correctAnswer: 0
        },
        {
          topic: 'טריגונומטריה',
          question: 'מה הוא sin(30°)?',
          answers: [
            '1/2',
            '√3/2',
            '√2/2',
            '1'
          ],
          correctAnswer: 0
        }
      ]
    };
  },
  computed: {
    topicScores() {
      const scores = {};
      const topicQuestions = {};
      
      // Initialize counters
      this.questions.forEach(q => {
        if (!scores[q.topic]) {
          scores[q.topic] = 0;
          topicQuestions[q.topic] = 0;
        }
        topicQuestions[q.topic]++;
      });

      // Calculate scores
      this.questions.forEach((q, index) => {
        if (this.userAnswers[index] === q.correctAnswer) {
          scores[q.topic]++;
        }
      });

      // Convert to percentages
      Object.keys(scores).forEach(topic => {
        scores[topic] = scores[topic] / topicQuestions[topic];
      });

      return scores;
    }
  },
  methods: {
    startQuiz() {
      this.quizStarted = true;
      this.userAnswers = new Array(this.questions.length).fill(null);
    },
    skipQuiz() {
      this.$emit('quiz-skipped');
      this.$router.push('/main');
    },
    selectAnswer(index) {
      this.selectedAnswer = index;
      this.userAnswers[this.currentQuestionIndex] = index;
    },
    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
        this.selectedAnswer = this.userAnswers[this.currentQuestionIndex];
      }
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++;
        this.selectedAnswer = this.userAnswers[this.currentQuestionIndex];
      }
    },
    finishQuiz() {
      this.quizCompleted = true;
      // Save quiz results to localStorage
      localStorage.setItem('quizResults', JSON.stringify({
        completed: true,
        scores: this.topicScores,
        timestamp: new Date().toISOString()
      }));
    },
    goToMainPage() {
      this.$router.push('/main');
    }
  }
};
</script> 