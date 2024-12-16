import { defineStore } from 'pinia';
import axios from 'axios';
import { useReadStatusStore } from './readStatus';

const API_BASE_URL = 'http://localhost:8001';

// 延迟函数
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 重试函数
async function fetchWithRetry(fn, retries = 3, delay = 2000) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      console.log(`Attempt ${i + 1} failed, retrying in ${delay}ms...`);
      await sleep(delay);
    }
  }
}

export const usePapersStore = defineStore('papers', {
  state: () => ({
    papers: [],
    categories: [],
    selectedCategory: null,
    readFilter: 'all',
    isLoading: false,
    error: null,
    isInitializing: true  // 新增：标记初始化状态
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
      this.error = null;
      
      try {
        const response = await fetchWithRetry(
          () => axios.get(`${API_BASE_URL}/papers/recent`, {
            params: {
              days: 7,
              limit: 100
            }
          }),
          3,  // 3次重试
          2000 // 2秒延迟
        );
        
        this.papers = response.data;
        this.isInitializing = false;
      } catch (error) {
        console.error('Error fetching papers:', error);
        this.error = 'Failed to fetch papers. The backend might still be starting up...';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchCategories() {
      try {
        const response = await fetchWithRetry(
          () => axios.get(`${API_BASE_URL}/papers/categories`),
          3,
          2000
        );
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