import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Define the initial state
const initialState = {
  translatedText: '',
  termMapping: '',
  models: [],
  languages: {},
  dictionaries: [],
  loading: false,
  error: null,
  fileTranslationLoading: false,
  fileTranslationError: null,
};

// Async thunks
export const translateText = createAsyncThunk(
  'translation/translateText',
  async (translationData, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.post('/api/v1/translation/text', translationData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Translation failed');
    }
  }
);

export const translateFile = createAsyncThunk(
  'translation/translateFile',
  async ({ file, target_lang, dictionary_id, model_id, concurrency, lambda_alias = 'staging' }, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      // 验证文件
      if (!file) {
        return rejectWithValue('未选择文件');
      }
      
      // 验证文件类型
      const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
                      file.type === 'application/vnd.ms-excel' ||
                      file.name.endsWith('.xlsx') ||
                      file.name.endsWith('.xls');
      
      if (!isExcel) {
        return rejectWithValue('只支持Excel文件格式(.xlsx, .xls)');
      }
      
      // 验证文件大小
      if (file.size > 10 * 1024 * 1024) { // 10MB
        return rejectWithValue('文件大小不能超过10MB');
      }
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('target_lang', target_lang);
      formData.append('dictionary_id', dictionary_id);
      formData.append('model_id', model_id);
      formData.append('concurrency', concurrency);
      formData.append('lambda_alias', lambda_alias);
      
      const response = await axios.post('/api/v1/translation/file', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });
      
      // 检查响应是否为错误消息
      const contentType = response.headers['content-type'];
      if (contentType && contentType.includes('application/json')) {
        // 如果是JSON响应，可能是错误信息
        const errorText = await new Response(response.data).text();
        const errorJson = JSON.parse(errorText);
        return rejectWithValue(errorJson.detail || '文件翻译失败');
      }
      
      // 创建下载链接
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `processed_${file.name}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      return { success: true };
    } catch (error) {
      // 尝试从错误响应中提取详细信息
      if (error.response) {
        if (error.response.data instanceof Blob) {
          try {
            // 尝试将Blob转换为文本以读取错误信息
            const text = await new Response(error.response.data).text();
            try {
              const errorData = JSON.parse(text);
              return rejectWithValue(errorData.detail || '文件翻译失败');
            } catch (e) {
              return rejectWithValue(text || '文件翻译失败');
            }
          } catch (e) {
            return rejectWithValue(`文件翻译失败: ${error.response.status} ${error.response.statusText}`);
          }
        }
        return rejectWithValue(error.response.data?.detail || `文件翻译失败: ${error.response.status}`);
      }
      return rejectWithValue(error.message || '文件翻译失败，请检查网络连接');
    }
  }
);

export const fetchModels = createAsyncThunk(
  'translation/fetchModels',
  async (_, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.get('/api/v1/translation/models', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      return response.data.models;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch models');
    }
  }
);

export const fetchLanguages = createAsyncThunk(
  'translation/fetchLanguages',
  async (_, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.get('/api/v1/translation/languages', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      return response.data.languages;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch languages');
    }
  }
);

export const fetchDictionaries = createAsyncThunk(
  'translation/fetchDictionaries',
  async (_, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.get('/api/v1/translation/dictionaries', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      return response.data.dictionaries;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch dictionaries');
    }
  }
);

// Create the slice
const translationSlice = createSlice({
  name: 'translation',
  initialState,
  reducers: {
    clearTranslation: (state) => {
      state.translatedText = '';
      state.termMapping = '';
    },
    clearError: (state) => {
      state.error = null;
      state.fileTranslationError = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Translate text
      .addCase(translateText.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(translateText.fulfilled, (state, action) => {
        state.loading = false;
        state.translatedText = action.payload.translated_text;
        state.termMapping = action.payload.term_mapping;
      })
      .addCase(translateText.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Translate file
      .addCase(translateFile.pending, (state) => {
        state.fileTranslationLoading = true;
        state.fileTranslationError = null;
      })
      .addCase(translateFile.fulfilled, (state) => {
        state.fileTranslationLoading = false;
      })
      .addCase(translateFile.rejected, (state, action) => {
        state.fileTranslationLoading = false;
        state.fileTranslationError = action.payload;
      })
      
      // Fetch models
      .addCase(fetchModels.fulfilled, (state, action) => {
        state.models = action.payload;
      })
      
      // Fetch languages
      .addCase(fetchLanguages.fulfilled, (state, action) => {
        state.languages = action.payload;
      })
      
      // Fetch dictionaries
      .addCase(fetchDictionaries.fulfilled, (state, action) => {
        state.dictionaries = action.payload;
      });
  },
});

export const { clearTranslation, clearError } = translationSlice.actions;

export default translationSlice.reducer;
