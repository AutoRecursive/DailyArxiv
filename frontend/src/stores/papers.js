import { defineStore } from 'pinia';
import axios from 'axios';
import { useReadStatusStore } from './readStatus';

const API_BASE_URL = 'http://localhost:8000';

export const usePapersStore = defineStore('papers', {
  state: () => ({
    papers: [],
    categories: [],
    selectedCategory: null,
    readFilter: 'all', // 'all' | 'read' | 'unread'
    isLoading: false,
    error: null
  }),

  getters: {
    filteredPapers: (state) => {
      let filtered = state.papers;
      
      // 分类过滤
      if (state.selectedCategory) {
        filtered = filtered.filter(paper => 
          paper.categories.includes(state.selectedCategory)
        );
      }
      
      // 阅读状态过滤
      if (state.readFilter !== 'all') {
        const readStatusStore = useReadStatusStore();
        filtered = filtered.filter(paper => {
          const isRead = readStatusStore.isRead(paper.id);
          return state.readFilter === 'read' ? isRead : !isRead;
        });
      }
      
      return filtered;
    }
  },

  actions: {
    async fetchPapers() {
      this.isLoading = true;
      try {
        const response = await axios.get(`${API_BASE_URL}/papers/recent`, {
          params: {
            days: 7,
            limit: 100
          }
        });
        this.papers = response.data;
        this.error = null;
      } catch (error) {
        console.error('Error fetching papers:', error);
        this.error = 'Failed to fetch papers';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchCategories() {
      try {
        const response = await axios.get(`${API_BASE_URL}/papers/categories`);
        this.categories = response.data;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },

    async updatePapers() {
      try {
        await axios.post(`${API_BASE_URL}/papers/update`);
        // 更新后重新获取数据
        await this.fetchPapers();
        await this.fetchCategories();
      } catch (error) {
        console.error('Error updating papers:', error);
      }
    },

    setSelectedCategory(category) {
      this.selectedCategory = category;
    },

    setReadFilter(filter) {
      this.readFilter = filter;
    }
  }
}); 