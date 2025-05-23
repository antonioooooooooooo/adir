<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">סטטיסטיקות אישיות</h2>
          <button
            @click="$emit('close')"
            class="text-gray-500 hover:text-gray-700"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Quiz Results Section -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold mb-3">תוצאות בחינת רמה</h3>
          <div v-if="quizResults" class="bg-gray-50 rounded-lg p-4">
            <div class="grid gap-2">
              <div v-for="(score, topic) in quizResults.scores" :key="topic" class="flex justify-between">
                <span>{{ topic }}</span>
                <span class="font-medium">{{ Math.round(score * 100) }}%</span>
              </div>
            </div>
            <div class="text-sm text-gray-500 mt-2">
              נבחן בתאריך: {{ new Date(quizResults.timestamp).toLocaleDateString('he-IL') }}
            </div>
          </div>
          <div v-else class="text-gray-500 text-center py-4">
            טרם ביצעת בחינת רמה
          </div>
        </div>

        <!-- Overall Statistics -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold mb-3">סטטיסטיקות כלליות</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-blue-50 rounded-lg p-4">
              <div class="text-2xl font-bold text-blue-600">{{ stats.totalQuestions }}</div>
              <div class="text-sm text-gray-600">שאלות שנפתרו</div>
            </div>
            <div class="bg-green-50 rounded-lg p-4">
              <div class="text-2xl font-bold text-green-600">{{ stats.correctAnswers }}</div>
              <div class="text-sm text-gray-600">תשובות נכונות</div>
            </div>
            <div class="bg-purple-50 rounded-lg p-4">
              <div class="text-2xl font-bold text-purple-600">{{ stats.hintsUsed }}</div>
              <div class="text-sm text-gray-600">רמזים שנעזרת בהם</div>
            </div>
            <div class="bg-yellow-50 rounded-lg p-4">
              <div class="text-2xl font-bold text-yellow-600">{{ formatTime(stats.totalTimeSpent) }}</div>
              <div class="text-sm text-gray-600">זמן למידה כולל</div>
            </div>
          </div>
        </div>

        <!-- Questions by Topic -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold mb-3">שאלות לפי נושא</h3>
          <div class="space-y-3">
            <div v-for="topic in stats.topicStats" :key="topic.name" class="bg-gray-50 rounded-lg p-4">
              <div class="flex justify-between items-center mb-2">
                <span class="font-medium">{{ topic.name }}</span>
                <span class="text-sm text-gray-600">{{ topic.total }} שאלות</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  class="bg-blue-600 h-2.5 rounded-full"
                  :style="{ width: `${topic.total > 0 ? (topic.correct / topic.total) * 100 : 0}%` }"
                ></div>
              </div>
              <div class="flex justify-between text-sm mt-1">
                <span class="text-gray-600">אחוז הצלחה: {{ topic.total > 0 ? Math.round((topic.correct / topic.total) * 100) : 0 }}%</span>
                <span class="text-gray-600">{{ topic.correct }}/{{ topic.total }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div>
          <h3 class="text-lg font-semibold mb-3">פעילות אחרונה</h3>
          <div class="space-y-2">
            <div v-for="(activity, index) in stats.recentActivity" :key="index" class="flex items-center gap-3 p-2 bg-gray-50 rounded">
              <div :class="[
                'w-2 h-2 rounded-full',
                activity.success ? 'bg-green-500' : 'bg-red-500'
              ]"></div>
              <div class="flex-1">{{ activity.topic }} - {{ activity.description }}</div>
              <div class="text-sm text-gray-500">{{ formatTimeAgo(activity.timestamp) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatisticsModal',
  props: {
    show: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      quizResults: JSON.parse(localStorage.getItem('quizResults')),
      stats: {
        totalQuestions: 0,
        correctAnswers: 0,
        hintsUsed: 0,
        totalTimeSpent: 0, // in minutes
        topicStats: [
          { name: 'בעיות תנועה', total: 0, correct: 0 },
          { name: 'סדרות', total: 0, correct: 0 },
          { name: 'הסתברות', total: 0, correct: 0 },
          { name: 'גיאומטריה', total: 0, correct: 0 },
          { name: 'טריגונומטריה', total: 0, correct: 0 }
        ],
        recentActivity: []
      }
    }
  },
  methods: {
    formatTime(minutes) {
      const hours = Math.floor(minutes / 60)
      const remainingMinutes = minutes % 60
      return `${hours}:${remainingMinutes.toString().padStart(2, '0')}`
    },
    formatTimeAgo(timestamp) {
      const now = new Date()
      const activityTime = new Date(timestamp)
      const diffInMinutes = Math.floor((now - activityTime) / 1000 / 60)

      if (diffInMinutes < 60) {
        return `לפני ${diffInMinutes} דקות`
      } else if (diffInMinutes < 1440) {
        const hours = Math.floor(diffInMinutes / 60)
        return `לפני ${hours} שעות`
      } else {
        const days = Math.floor(diffInMinutes / 1440)
        return `לפני ${days} ימים`
      }
    },
    loadStats() {
      // Load stats from localStorage
      const savedStats = localStorage.getItem('userStats')
      if (savedStats) {
        this.stats = JSON.parse(savedStats)
      }
    }
  },
  mounted() {
    this.loadStats()
  }
}
</script> 