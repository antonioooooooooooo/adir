<template>
  <div class="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4">בדוק את הפיתרון שלך</h2>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">העלה את קובץ הפיתרון שלך</label>
        <input
          type="file"
          accept="image/*"
          @change="handleFileChange"
          class="w-full p-2 border border-gray-300 rounded-md"
        />
      </div>

      <button
        type="submit"
        :disabled="loading || !file"
        :class="[
          'w-full py-2 px-4 rounded-md text-white font-medium',
          loading || !file ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700',
        ]"
      >
        {{ loading ? 'בודק...' : 'בדוק פיתרון' }}
      </button>
    </form>

    <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ error }}
    </div>

    <div v-if="result" class="mt-4 space-y-2">
      <div
        :class="[
          'p-3 rounded',
          result.isCorrect
            ? 'bg-green-100 border border-green-400 text-green-700'
            : 'bg-yellow-100 border border-yellow-400 text-yellow-700',
        ]"
      >
        {{ result.isCorrect ? 'Your solution is correct!' : 'Your solution needs work' }}
      </div>

      <div class="mt-2">
        <h3 class="font-medium text-gray-700">Extracted Text:</h3>
        <p class="mt-1 p-2 bg-gray-50 rounded text-sm">
          {{ result.extractedText || 'No text extracted' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'SolutionUpload',
    data() {
      return {
        file: null,
        result: null,
        loading: false,
        error: null,
      };
    },
    methods: {
      handleFileChange(e) {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
          this.file = selectedFile;
          this.error = null;
          this.result = null;
        }
      },
      async handleSubmit() {
        if (!this.file) {
          this.error = 'Please select a file first';
          return;
        }

        this.loading = true;
        this.error = null;

        const formData = new FormData();
        formData.append('solution', this.file);

        try {
          const response = await fetch('http://localhost:5001/api/verify-solution', {
            method: 'POST',
            body: formData,
          });

          const data = await response.json();

          if (!response.ok) {
            throw new Error(data.error || 'Failed to verify solution');
          }

          this.result = data;
        } catch (err) {
          this.error = err.message;
        } finally {
          this.loading = false;
        }
      },
    },
  };
</script>
