<template>
  <div class="paper-grid">
    <div v-if="isLoading || store.isInitializing" class="loading">
      <p>{{ loadingMessage }}</p>
      <div class="loading-spinner"></div>
    </div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button class="retry-button" @click="retryFetch">Retry</button>
    </div>
    <div v-else-if="papers.length === 0" class="no-papers">
      No papers found. Try refreshing or changing filters.
    </div>
    <template v-else>
      <PaperCard
        v-for="paper in papers"
        :key="paper.id"
        :paper="paper"
      />
    </template>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { usePapersStore } from '../stores/papers';
import PaperCard from './PaperCard.vue';

const store = usePapersStore();
const startTime = ref(Date.now());

const loadingMessage = computed(() => {
  const elapsed = Math.floor((Date.now() - startTime.value) / 1000);
  if (elapsed < 5) {
    return 'Loading papers...';
  } else {
    return 'Starting backend service... This might take a few seconds.';
  }
});

async function retryFetch() {
  startTime.value = Date.now();
  await store.fetchPapers();
}

onMounted(async () => {
  await store.fetchPapers();
});

const papers = computed(() => store.filteredPapers);
const isLoading = computed(() => store.isLoading);
const error = computed(() => store.error);
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.paper-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: $spacing-unit * 2;
  padding: $spacing-unit * 2;
}

.loading, .error, .no-papers {
  grid-column: 1 / -1;
  text-align: center;
  padding: $spacing-unit * 4;
  @include themed() {
    background: t('card-background');
  }
  border-radius: $card-border-radius;
}

.error {
  @include themed() {
    color: t('primary-color');
  }
}

.loading-spinner {
  margin: $spacing-unit * 2 auto;
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.retry-button {
  margin-top: $spacing-unit * 2;
  padding: $spacing-unit $spacing-unit * 2;
  border-radius: $card-border-radius;
  cursor: pointer;
  @include themed() {
    background: t('primary-color');
    color: t('card-background');
    border: none;
    
    &:hover {
      background: t('secondary-color');
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 