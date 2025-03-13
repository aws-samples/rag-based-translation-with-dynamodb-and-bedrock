import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Define the initial state
const initialState = {
  parameters: [],
  loading: false,
  error: null,
  updateSuccess: false,
};

// Async thunks
export const fetchParameters = createAsyncThunk(
  'parameter/fetchParameters',
  async (path, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      const response = await axios.get(`/api/v1/parameters/by-path/${path}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      return response.data.parameters;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch parameters');
    }
  }
);

export const updateParameter = createAsyncThunk(
  'parameter/updateParameter',
  async ({ name, value }, { getState, rejectWithValue }) => {
    try {
      const { token } = getState().auth;
      
      await axios.put(`/api/v1/parameters/${name}`, { value }, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      return { name, value };
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update parameter');
    }
  }
);

// Create the slice
const parameterSlice = createSlice({
  name: 'parameter',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearUpdateSuccess: (state) => {
      state.updateSuccess = false;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch parameters
      .addCase(fetchParameters.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchParameters.fulfilled, (state, action) => {
        state.loading = false;
        state.parameters = action.payload;
      })
      .addCase(fetchParameters.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Update parameter
      .addCase(updateParameter.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.updateSuccess = false;
      })
      .addCase(updateParameter.fulfilled, (state, action) => {
        state.loading = false;
        state.updateSuccess = true;
        
        // Update the parameter in the list
        const index = state.parameters.findIndex(p => p.Name === action.payload.name);
        if (index !== -1) {
          state.parameters[index].Value = action.payload.value;
        }
      })
      .addCase(updateParameter.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.updateSuccess = false;
      });
  },
});

export const { clearError, clearUpdateSuccess } = parameterSlice.actions;

export default parameterSlice.reducer;
