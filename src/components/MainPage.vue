<template>
  <main class="min-h-screen bg-gray-50" dir="rtl">
    <header class="bg-blue-600 text-white p-6 shadow-lg">
      <h1 class="text-3xl font-bold">מתרגל בגרות במתמטיקה - 5 יח"ל</h1>
      <p class="mt-2 text-blue-100">תרגול שאלות וקבלת עזרה מיידית</p>
      
      <!-- User info and controls -->
      <div class="mt-2 flex justify-between items-center">
        <div class="text-sm flex items-center gap-4">
          <span>שלום {{ userInfo.name }}</span>
          <button @click="showStats = true" class="text-blue-200 hover:text-white flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            סטטיסטיקות
          </button>
          <button @click="logout" class="text-blue-200 hover:text-white">התנתק</button>
        </div>
        <div v-if="!quizResults" class="text-sm">
          <button 
            @click="startQuiz" 
            class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-400"
          >
            בצע בחינת רמה
          </button>
        </div>
        <div v-else class="text-sm">
          <span class="text-blue-200">רמה נקבעה | </span>
          <button 
            @click="startQuiz" 
            class="text-blue-200 hover:text-white"
          >
            בצע בחינה מחדש
          </button>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Topic Selection and Controls -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold mb-4">בחר נושא</h2>
            <select v-model="selectedTopic" class="w-full p-2 border rounded-md mb-4">
              <option v-for="topic in topics" :key="topic.id" :value="topic.id">
                {{ topic.name }}
              </option>
            </select>
            <button
              @click="generateQuestion"
              :disabled="isLoading"
              class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:bg-blue-400"
            >
              {{ isLoading ? 'טוען...' : 'צור שאלה חדשה' }}
            </button>
          </div>
        </div>

        <!-- Question and Interaction Area -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-xl font-semibold mb-4">שאלה נוכחית</h2>
            <div class="bg-gray-50 p-4 rounded-md mb-4 whitespace-pre-line">
              {{ currentQuestion || 'לחץ על "צור שאלה חדשה" כדי להתחיל' }}
            </div>

            <div class="flex gap-4 mb-6">
              <button
                @click="requestHint"
                :disabled="isLoading || !currentQuestion"
                class="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors disabled:bg-green-400"
              >
                {{ isLoading ? 'טוען...' : 'קבל רמז' }}
              </button>
              <button
                @click="toggleSolution"
                :disabled="isLoading || !currentQuestion"
                class="flex-1 bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 transition-colors disabled:bg-purple-400"
              >
                {{ isLoading ? 'טוען...' : showSolution ? 'הסתר פתרון' : 'הצג פתרון' }}
              </button>
            </div>

            <!-- Hints Section -->
            <div v-if="hints.length" class="mb-6">
              <h3 class="font-semibold mb-2">רמזים:</h3>
              <ul class="list-disc pr-6">
                <li v-for="(hint, index) in hints" :key="index" class="text-gray-700">
                  {{ hint }}
                </li>
              </ul>
            </div>

            <!-- Solution Section -->
            <div v-if="showSolution" class="mb-6">
              <h3 class="font-semibold mb-2">פתרון:</h3>
              <div class="bg-gray-50 p-4 rounded-md whitespace-pre-line">{{ solution }}</div>
            </div>

            <!-- Solution Upload Section -->
            <div v-if="currentQuestion" class="border-t pt-6 mb-6">
              <h3 class="font-semibold mb-4">העלה את הפתרון שלך</h3>
              <SolutionUpload />
            </div>

            <!-- Chat Section -->
            <div class="border-t pt-6">
              <h3 class="font-semibold mb-4">שאל שאלה</h3>
              <div class="mb-4 max-h-60 overflow-y-auto">
                <div
                  v-for="(message, index) in messages"
                  :key="index"
                  :class="[
                    'mb-2 p-3 rounded-lg',
                    message.isUser ? 'bg-blue-100 mr-auto' : 'bg-gray-100',
                  ]"
                  :style="{ maxWidth: '80%' }"
                >
                  {{ message.text }}
                </div>
              </div>
              <div class="flex gap-2">
                <input
                  v-model="userMessage"
                  @keyup.enter="sendMessage"
                  :disabled="isLoading"
                  type="text"
                  placeholder="הקלד את שאלתך כאן..."
                  class="flex-1 p-2 border rounded-md"
                />
                <button
                  @click="sendMessage"
                  :disabled="isLoading"
                  class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:bg-blue-400"
                >
                  {{ isLoading ? 'שולח...' : 'שלח' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Statistics Modal -->
    <StatisticsModal
      :show="showStats"
      @close="showStats = false"
    />
  </main>
</template>

<script>
import { ref, onMounted } from 'vue';
import SolutionUpload from './SolutionUpload.vue';
import StatisticsModal from './StatisticsModal.vue';
import { useRouter } from 'vue-router';

export default {
  name: 'MainPage',
  components: {
    SolutionUpload,
    StatisticsModal
  },
  setup() {
    const router = useRouter();
    const API_BASE_URL = 'http://localhost:5001/api';
    const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || '{}'));
    const quizResults = ref(JSON.parse(localStorage.getItem('quizResults') || null));
    const showStats = ref(false);
    
    const selectedTopic = ref('traffic');
    const currentQuestion = ref('');
    const showSolution = ref(false);
    const hints = ref([]);
    const messages = ref([]);
    const userMessage = ref('');
    const isLoading = ref(false);
    const solution = ref('');

    const topics = [
      { id: 'traffic', name: 'בעיות תנועה' },
      { id: 'series', name: 'סדרות' },
      { id: 'probability', name: 'הסתברות' },
      { id: 'geometry', name: 'גיאומטריה' },
      { id: 'trigonometry', name: 'טריגונומטריה' },
      { id: 'calculus', name: 'חשבון דיפרנציאלי ואינטגרלי' },
    ];

    const logout = () => {
      localStorage.removeItem('userInfo');
      router.push('/register');
    };

    const updateStats = (action, data) => {
      const stats = JSON.parse(localStorage.getItem('userStats') || '{}');
      const now = new Date();

      // Initialize stats if they don't exist
      if (!stats.totalQuestions) {
        stats.totalQuestions = 0;
        stats.correctAnswers = 0;
        stats.hintsUsed = 0;
        stats.totalTimeSpent = 0;
        stats.topicStats = [
          { name: 'בעיות תנועה', total: 0, correct: 0 },
          { name: 'סדרות', total: 0, correct: 0 },
          { name: 'הסתברות', total: 0, correct: 0 },
          { name: 'גיאומטריה', total: 0, correct: 0 },
          { name: 'טריגונומטריה', total: 0, correct: 0 }
        ];
        stats.recentActivity = [];
      }

      switch (action) {
        case 'question_attempted':
          stats.totalQuestions++;
          const topicStat = stats.topicStats.find(t => t.name === data.topic);
          if (topicStat) {
            topicStat.total++;
            if (data.correct) topicStat.correct++;
          }
          stats.recentActivity.unshift({
            topic: data.topic,
            description: data.correct ? 'פתרת נכון' : 'טעות',
            success: data.correct,
            timestamp: now.toISOString()
          });
          break;
        case 'hint_used':
          stats.hintsUsed++;
          stats.recentActivity.unshift({
            topic: data.topic,
            description: 'השתמשת ברמז',
            success: true,
            timestamp: now.toISOString()
          });
          break;
        case 'time_spent':
          stats.totalTimeSpent += data.minutes;
          break;
      }

      // Keep only last 10 activities
      stats.recentActivity = stats.recentActivity.slice(0, 10);

      localStorage.setItem('userStats', JSON.stringify(stats));
    };

    const generateQuestion = async () => {
      try {
        isLoading.value = true;
        const response = await fetch(`${API_BASE_URL}/question`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            category: selectedTopic.value,
            hebrew: true,
          }),
        });
        const data = await response.json();
        currentQuestion.value = data.question;
        showSolution.value = false;
        hints.value = [];
        solution.value = '';
        updateStats('question_attempted', { topic: selectedTopic.value });
      } catch (error) {
        console.error('Error generating question:', error);
        currentQuestion.value = 'שגיאה ביצירת השאלה. אנא נסה שוב.';
      } finally {
        isLoading.value = false;
      }
    };

    const requestHint = async () => {
      try {
        isLoading.value = true;
        const response = await fetch(`${API_BASE_URL}/hint`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: currentQuestion.value,
          }),
        });
        const data = await response.json();
        hints.value.push(data.hint);
        updateStats('hint_used', { topic: selectedTopic.value });
      } catch (error) {
        console.error('Error getting hint:', error);
        hints.value.push('שגיאה בקבלת הרמז. אנא נסה שוב.');
      } finally {
        isLoading.value = false;
      }
    };

    const toggleSolution = async () => {
      if (!showSolution.value && !solution.value) {
        try {
          isLoading.value = true;
          const response = await fetch(`${API_BASE_URL}/solution`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              question: currentQuestion.value,
              explain: true,
            }),
          });
          const data = await response.json();
          solution.value = data.solution;
        } catch (error) {
          console.error('Error getting solution:', error);
          solution.value = 'שגיאה בקבלת הפתרון. אנא נסה שוב.';
        } finally {
          isLoading.value = false;
        }
      }
      showSolution.value = !showSolution.value;
    };

    const sendMessage = async () => {
      if (userMessage.value.trim()) {
        const userMsg = `This is the question the user is trying to solve for context:\n${currentQuestion.value}\nAnd this is their message:\n${userMessage.value}`;
        messages.value.push({
          text: userMsg,
          isUser: true,
        });
        userMessage.value = '';

        try {
          isLoading.value = true;
          const response = await fetch(`${API_BASE_URL}/hint`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              question: userMsg,
            }),
          });
          const data = await response.json();
          messages.value.push({
            text: data.hint,
            isUser: false,
          });
        } catch (error) {
          console.error('Error getting response:', error);
          messages.value.push({
            text: 'שגיאה בקבלת תשובה. אנא נסה שוב.',
            isUser: false,
          });
        } finally {
          isLoading.value = false;
        }
      }
    };

    const startQuiz = () => {
      router.push('/quiz');
    };

    // Track time spent
    let startTime = Date.now();
    setInterval(() => {
      const timeSpent = Math.floor((Date.now() - startTime) / 1000 / 60); // Convert to minutes
      if (timeSpent > 0) {
        updateStats('time_spent', { minutes: 1 });
        startTime = Date.now();
      }
    }, 60000); // Check every minute

    onMounted(() => {
      if (!localStorage.getItem('userInfo')) {
        router.push('/register');
      }
    });

    return {
      userInfo,
      quizResults,
      showStats,
      selectedTopic,
      currentQuestion,
      showSolution,
      hints,
      messages,
      userMessage,
      isLoading,
      solution,
      topics,
      logout,
      startQuiz,
      generateQuestion,
      requestHint,
      toggleSolution,
      sendMessage,
      updateStats
    };
  },
};
</script> 