<template>
  <div class="read-status-filter">
    <h3 class="filter-header">Reading Status</h3>
    <div class="filter-content">
      <div class="filter-buttons">
        <button
          v-for="option in filterOptions"
          :key="option.value"
          :class="['filter-btn', { active: currentFilter === option.value }]"
          @click="setFilter(option.value)"
        >
          {{ option.label }}
          <span class="count">({{ getCount(option.value) }})</span>
        </button>
      </div>
      <div class="actions">
        <button class="action-btn" @click="markAllAsRead">
          Mark All as Read
        </button>
        <button class="action-btn" @click="clearAllReadStatus">
          Clear Read Status
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { usePapersStore } from '../stores/papers';
import { useReadStatusStore } from '../stores/readStatus';

const papersStore = usePapersStore();
const readStatusStore = useReadStatusStore();

const filterOptions = [
  { value: 'all', label: 'All Papers' },
  { value: 'unread', label: 'Unread' },
  { value: 'read', label: 'Read' }
];

const currentFilter = computed(() => papersStore.readFilter);

function setFilter(filter) {
  papersStore.setReadFilter(filter);
}

function getCount(filter) {
  if (filter === 'all') return papersStore.papers.length;
  if (filter === 'read') return readStatusStore.readCount;
  return papersStore.papers.length - readStatusStore.readCount;
}

function markAllAsRead() {
  const paperIds = papersStore.papers.map(p => p.id);
  readStatusStore.markAllAsRead(paperIds);
}

function clearAllReadStatus() {
  if (confirm('Are you sure you want to clear all read status?')) {
    readStatusStore.clearAllReadStatus();
  }
}
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.read-status-filter {
  display: flex;
  flex-direction: column;
  height: 100%;
  
  .filter-header {
    padding: $spacing-unit * 2;
    margin: 0;
    @include themed() {
      color: t('text-primary');
    }
  }
  
  .filter-content {
    flex: 1;
    overflow-y: auto;
    padding: 0 $spacing-unit * 2 $spacing-unit * 2;
    
    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-track {
      @include themed() {
        background: t('background-color');
      }
    }

    &::-webkit-scrollbar-thumb {
      @include themed() {
        background: t('border-color');
        &:hover {
          background: t('text-secondary');
        }
      }
      border-radius: 2px;
    }
  }
}

.filter-buttons {
  display: flex;
  flex-direction: column;
  gap: $spacing-unit;
  margin-bottom: $spacing-unit * 2;
}

.filter-btn {
  padding: $spacing-unit $spacing-unit * 2;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  
  @include themed() {
    background: t('category-bg');
    color: t('category-text');
    border: 1px solid t('category-text');
    
    &:hover {
      background: rgba(t('category-text'), 0.2);
    }
    
    &.active {
      background: t('primary-color');
      color: t('card-background');
      border-color: t('primary-color');
    }
  }

  .count {
    opacity: 0.7;
    margin-left: 4px;
  }
}

.actions {
  margin-top: $spacing-unit * 2;
  display: flex;
  flex-direction: column;
  gap: $spacing-unit;
}

.action-btn {
  padding: $spacing-unit;
  border-radius: $card-border-radius;
  cursor: pointer;
  transition: all 0.2s;
  
  @include themed() {
    background: t('card-background');
    color: t('text-primary');
    border: 1px solid t('border-color');
    
    &:hover {
      background: t('border-color');
    }
  }
}
</style> 