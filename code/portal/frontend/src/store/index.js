import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import translationReducer from './slices/translationSlice';
import dictionaryReducer from './slices/dictionarySlice';
import parameterReducer from './slices/parameterSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    translation: translationReducer,
    dictionary: dictionaryReducer,
    parameter: parameterReducer,
  },
});
