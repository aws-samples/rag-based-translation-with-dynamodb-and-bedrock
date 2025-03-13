import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Define the initial state
const initialState = {
  dictionaries: [],
  dictionaryVersions: {},
  currentTerm: null,
  loading: false,
  error: null,
  uploadLoading: false,
  uploadError: null,
  uploadSuccess: false,
  jobStatus: null,
  qualityCheckResult: null,
};

// Async thunks
export const fetchDictionaries = createAsyncThunk(
  'dictionary/fetchDictionaries',
  async (_, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.get('/api/v1/dictionary/list', {
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

export const fetchDictionaryVersions = createAsyncThunk(
  'dictionary/fetchDictionaryVersions',
  async (_, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.get('/api/v1/dictionary/versions', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      return response.data.dictionary_versions;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch dictionary versions');
    }
  }
);

export const fetchDictionaryTerm = createAsyncThunk(
  'dictionary/fetchDictionaryTerm',
  async ({ dictionaryName, term }, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.get(`/api/v1/dictionary/term/${dictionaryName}/${term}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch dictionary term');
    }
  }
);

export const updateDictionaryTerm = createAsyncThunk(
  'dictionary/updateDictionaryTerm',
  async ({ dictionaryName, term, termData }, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      await axios.put(`/api/v1/dictionary/term/${dictionaryName}/${term}`, termData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      return { dictionaryName, term, ...termData };
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update dictionary term');
    }
  }
);

export const updateDictionaryVersion = createAsyncThunk(
  'dictionary/updateDictionaryVersion',
  async ({ dictId, version }, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      await axios.put(`/api/v1/dictionary/current-version/${dictId}`, { version }, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      return { dictId, version };
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update dictionary version');
    }
  }
);

export const uploadDictionary = createAsyncThunk(
  'dictionary/uploadDictionary',
  async ({ file, dictionaryName, isNew, version }, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('dictionary_name', dictionaryName);
      formData.append('is_new', isNew);
      if (version) {
        formData.append('version', version);
      }
      
      const response = await axios.post('/api/v1/dictionary/upload', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      if (error.response?.data?.errors) {
        return rejectWithValue({
          message: error.response.data.message,
          errors: error.response.data.errors,
        });
      }
      return rejectWithValue(error.response?.data?.detail || 'Failed to upload dictionary');
    }
  }
);

export const checkDictionaryJobStatus = createAsyncThunk(
  'dictionary/checkDictionaryJobStatus',
  async (runId, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.get(`/api/v1/dictionary/job-status/${runId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to check job status');
    }
  }
);

export const checkDictionaryQuality = createAsyncThunk(
  'dictionary/checkDictionaryQuality',
  async (file, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post('/api/v1/dictionary/quality-check', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to check dictionary quality');
    }
  }
);

// Create the slice
const dictionarySlice = createSlice({
  name: 'dictionary',
  initialState,
  reducers: {
    clearCurrentTerm: (state) => {
      state.currentTerm = null;
    },
    clearError: (state) => {
      state.error = null;
      state.uploadError = null;
    },
    clearUploadSuccess: (state) => {
      state.uploadSuccess = false;
    },
    clearQualityCheckResult: (state) => {
      state.qualityCheckResult = null;
    },
    clearJobStatus: (state) => {
      state.jobStatus = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch dictionaries
      .addCase(fetchDictionaries.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDictionaries.fulfilled, (state, action) => {
        state.loading = false;
        state.dictionaries = action.payload;
      })
      .addCase(fetchDictionaries.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Fetch dictionary versions
      .addCase(fetchDictionaryVersions.fulfilled, (state, action) => {
        state.dictionaryVersions = action.payload;
      })
      
      // Fetch dictionary term
      .addCase(fetchDictionaryTerm.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDictionaryTerm.fulfilled, (state, action) => {
        state.loading = false;
        state.currentTerm = action.payload;
      })
      .addCase(fetchDictionaryTerm.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.currentTerm = null;
      })
      
      // Update dictionary term
      .addCase(updateDictionaryTerm.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateDictionaryTerm.fulfilled, (state, action) => {
        state.loading = false;
        state.currentTerm = action.payload;
      })
      .addCase(updateDictionaryTerm.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Upload dictionary
      .addCase(uploadDictionary.pending, (state) => {
        state.uploadLoading = true;
        state.uploadError = null;
        state.uploadSuccess = false;
      })
      .addCase(uploadDictionary.fulfilled, (state, action) => {
        state.uploadLoading = false;
        state.uploadSuccess = true;
        state.jobStatus = {
          runId: action.payload.run_id,
          status: 'STARTING',
        };
      })
      .addCase(uploadDictionary.rejected, (state, action) => {
        state.uploadLoading = false;
        state.uploadError = action.payload;
        state.uploadSuccess = false;
      })
      
      // Check dictionary job status
      .addCase(checkDictionaryJobStatus.fulfilled, (state, action) => {
        // Map the API response to the expected format
        state.jobStatus = {
          runId: action.payload.run_id,
          status: action.payload.status
        };
      })
      
      // Check dictionary quality
      .addCase(checkDictionaryQuality.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(checkDictionaryQuality.fulfilled, (state, action) => {
        state.loading = false;
        state.qualityCheckResult = action.payload;
      })
      .addCase(checkDictionaryQuality.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearCurrentTerm, clearError, clearUploadSuccess, clearQualityCheckResult, clearJobStatus } = dictionarySlice.actions;

export default dictionarySlice.reducer;
