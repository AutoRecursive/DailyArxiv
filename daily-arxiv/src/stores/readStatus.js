import { defineStore } from 'pinia';

const STORAGE_KEY = 'arxiv-read-papers';

export const useReadStatusStore = defineStore('readStatus', {
  state: () => ({
    readPapers: JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
  }),

  getters: {
    isRead: (state) => (paperId) => !!state.readPapers[paperId],
    
    readCount: (state) => Object.keys(state.readPapers).length,
    
    getReadTime: (state) => (paperId) => state.readPapers[paperId]?.readAt
  },

  actions: {
    toggleRead(paperId) {
      if (this.readPapers[paperId]) {
        delete this.readPapers[paperId];
      } else {
        this.readPapers[paperId] = {
          readAt: new Date().toISOString(),
          lastVisited: new Date().toISOString()
        };
      }
      this.saveToStorage();
    },

    markAsRead(paperId) {
      if (!this.readPapers[paperId]) {
        this.readPapers[paperId] = {
          readAt: new Date().toISOString(),
          lastVisited: new Date().toISOString()
        };
        this.saveToStorage();
      }
    },

    markAllAsRead(paperIds) {
      const now = new Date().toISOString();
      paperIds.forEach(id => {
        this.readPapers[id] = {
          readAt: now,
          lastVisited: now
        };
      });
      this.saveToStorage();
    },

    clearAllReadStatus() {
      this.readPapers = {};
      this.saveToStorage();
    },

    saveToStorage() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.readPapers));
    }
  }
}); 