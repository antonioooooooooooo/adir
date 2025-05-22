<script setup>
  import { ref } from 'vue';

  const selectedTopic = ref('calculus');
  const currentQuestion = ref('');
  const showSolution = ref(false);
  const hints = ref([]);
  const messages = ref([]);
  const userMessage = ref('');

  const topics = [
    { id: 'calculus', name: 'חשבון דיפרנציאלי ואינטגרלי' },
    { id: 'complex', name: 'מספרים מרוכבים' },
    { id: 'trigonometry', name: 'טריגונומטריה' },
    { id: 'probability', name: 'הסתברות וסטטיסטיקה' },
    { id: 'series', name: 'סדרות' },
  ];

  const generateQuestion = () => {
    // TODO: Implement API call to generate question
    currentQuestion.value = 'שאלה לדוגמה - תוחלף בתוכן שייווצר על ידי בינה מלאכותית';
    showSolution.value = false;
    hints.value = [];
  };

  const requestHint = () => {
    // TODO: Implement API call to get hint
    hints.value.push('רמז לדוגמה - יוחלף בתוכן שייווצר על ידי בינה מלאכותית');
  };

  const toggleSolution = () => {
    showSolution.value = !showSolution.value;
  };

  const sendMessage = () => {
    if (userMessage.value.trim()) {
      messages.value.push({
        text: userMessage.value,
        isUser: true,
      });
      // TODO: Implement API call to get response
      messages.value.push({
        text: 'תשובת המערכת תופיע כאן',
        isUser: false,
      });
      userMessage.value = '';
    }
  };
</script>

<template>
  <main class="min-h-screen bg-gray-50" dir="rtl">
    <header class="bg-blue-600 text-white p-6 shadow-lg">
      <h1 class="text-3xl font-bold">מתרגל בגרות במתמטיקה - 5 יח"ל</h1>
      <p class="mt-2 text-blue-100">תרגול שאלות וקבלת עזרה מיידית</p>
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
              class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
            >
              צור שאלה חדשה
            </button>
          </div>
        </div>

        <!-- Question and Interaction Area -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-xl font-semibold mb-4">שאלה נוכחית</h2>
            <div class="bg-gray-50 p-4 rounded-md mb-4">
              {{ currentQuestion || 'לחץ על "צור שאלה חדשה" כדי להתחיל' }}
            </div>

            <div class="flex gap-4 mb-6">
              <button
                @click="requestHint"
                class="flex-1 bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
              >
                קבל רמז
              </button>
              <button
                @click="toggleSolution"
                class="flex-1 bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 transition-colors"
              >
                {{ showSolution ? 'הסתר פתרון' : 'הצג פתרון' }}
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
              <div class="bg-gray-50 p-4 rounded-md">פתרון מפורט יופיע כאן</div>
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
                  type="text"
                  placeholder="הקלד את שאלתך כאן..."
                  class="flex-1 p-2 border rounded-md"
                />
                <button
                  @click="sendMessage"
                  class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
                >
                  שלח
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
  @import url('./assets/tailwind.css');
  @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700&display=swap');

  :root {
    font-family: 'Heebo', sans-serif;
  }
</style>
