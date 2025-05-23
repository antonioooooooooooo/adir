<template>
  <div class="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4">ברוך הבא! אנא מלא את הפרטים הבאים</h2>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">שם</label>
        <input
          type="text"
          v-model="userInfo.name"
          class="w-full p-2 border border-gray-300 rounded-md"
          required
          placeholder="השם שלך"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">גיל</label>
        <input
          type="number"
          v-model="userInfo.age"
          class="w-full p-2 border border-gray-300 rounded-md"
          required
          min="1"
          max="120"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">מגדר</label>
        <select
          v-model="userInfo.gender"
          class="w-full p-2 border border-gray-300 rounded-md"
          required
        >
          <option value="">בחר מגדר</option>
          <option value="male">זכר</option>
          <option value="female">נקבה</option>
          <option value="other">אחר</option>
        </select>
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">השכלה</label>
        <select
          v-model="userInfo.education"
          class="w-full p-2 border border-gray-300 rounded-md"
          required
        >
          <option value="">בחר רמת השכלה</option>
          <option value="high_school">תיכון</option>
          <option value="bachelor">תואר ראשון</option>
          <option value="master">תואר שני</option>
          <option value="phd">דוקטורט</option>
          <option value="other">אחר</option>
        </select>
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">תחום לימודים</label>
        <input
          type="text"
          v-model="userInfo.fieldOfStudy"
          class="w-full p-2 border border-gray-300 rounded-md"
          required
          placeholder="למשל: מתמטיקה, פיזיקה, מדעי המחשב"
        />
      </div>

      <button
        type="submit"
        class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md"
      >
        המשך
      </button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Registration',
  data() {
    return {
      userInfo: {
        name: '',
        age: null,
        gender: '',
        education: '',
        fieldOfStudy: ''
      }
    }
  },
  methods: {
    handleSubmit() {
      // Save user info to local storage
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo));
      // Redirect to quiz
      this.$router.push('/quiz');
    }
  }
}
</script> 