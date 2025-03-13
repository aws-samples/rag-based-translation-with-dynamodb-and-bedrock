import React, { useEffect, useState } from 'react';
import { 
  Card, 
  Upload, 
  Button, 
  Select, 
  Slider, 
  Typography, 
  Alert, 
  Spin,
  message
} from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';

import { 
  translateFile, 
  fetchModels, 
  fetchLanguages, 
  fetchDictionaries,
  clearError
} from '../store/slices/translationSlice';

const { Title, Text } = Typography;

const ExcelTranslatePage = () => {
  const dispatch = useDispatch();
  const { 
    models, 
    languages, 
    dictionaries, 
    fileTranslationLoading, 
    fileTranslationError 
  } = useSelector((state) => state.translation);

  const [file, setFile] = useState(null);
  const [targetLang, setTargetLang] = useState('');
  const [modelId, setModelId] = useState('');
  const [dictionaryId, setDictionaryId] = useState('');
  const [concurrency, setConcurrency] = useState(3);
  const [lambdaAlias, setLambdaAlias] = useState('staging');

  useEffect(() => {
    dispatch(fetchModels());
    dispatch(fetchLanguages());
    dispatch(fetchDictionaries());

    return () => {
      dispatch(clearError());
    };
  }, [dispatch]);

  useEffect(() => {
    if (languages && Object.keys(languages).length > 0) {
      const langKeys = Object.keys(languages);
      setTargetLang(languages[langKeys[0]]);
    }
  }, [languages]);

  useEffect(() => {
    if (models && models.length > 0) {
      setModelId(models[0]);
    }
  }, [models]);

  useEffect(() => {
    if (dictionaries && dictionaries.length > 0) {
      setDictionaryId(dictionaries[0]);
    }
  }, [dictionaries]);

  const handleFileChange = (info) => {
    if (info.file.status === 'done') {
      message.success(`${info.file.name} 上传成功`);
      setFile(info.file.originFileObj);
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} 上传失败`);
    }
  };

  const handleTranslate = () => {
    if (!file) {
      message.warning('请先上传Excel文件');
      return;
    }

    dispatch(translateFile({
      file,
      target_lang: targetLang,
      dictionary_id: dictionaryId,
      model_id: modelId,
      concurrency,
      lambda_alias: lambdaAlias
    }));
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    accept: '.xlsx, .xls',
    maxCount: 1,
    beforeUpload: (file) => {
      // 检查文件类型
      const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
                      file.type === 'application/vnd.ms-excel' ||
                      file.name.endsWith('.xlsx') ||
                      file.name.endsWith('.xls');
      
      // 检查文件大小 (限制为10MB)
      const isLessThan10M = file.size / 1024 / 1024 < 10;
      
      if (!isExcel) {
        message.error('只能上传Excel文件!');
        return Upload.LIST_IGNORE;
      }
      
      if (!isLessThan10M) {
        message.error('文件必须小于10MB!');
        return Upload.LIST_IGNORE;
      }
      
      return true;
    },
    customRequest: ({ file, onSuccess }) => {
      setTimeout(() => {
        onSuccess('ok');
      }, 0);
    },
    onChange: handleFileChange,
  };

  return (
    <div className="translation-container">
      <Title level={2}>Excel 文件语言处理器</Title>
      
      {fileTranslationError && (
        <Alert
          message="文件翻译错误"
          description={fileTranslationError}
          type="error"
          showIcon
          closable
          onClose={() => dispatch(clearError())}
          style={{ marginBottom: 16 }}
        />
      )}

      <Card>
        <div className="file-upload-container">
          <Upload {...uploadProps}>
            <Button icon={<UploadOutlined />}>选择Excel文件</Button>
          </Upload>
          <Text type="secondary" style={{ display: 'block', marginTop: 8 }}>
            支持 .xlsx, .xls 格式
          </Text>
        </div>

        <div style={{ marginBottom: 16 }}>
          <Text strong>目标语言</Text>
          <Select
            style={{ width: '100%', marginTop: 8 }}
            placeholder="目标语言"
            value={targetLang}
            onChange={setTargetLang}
            options={Object.entries(languages).map(([label, value]) => ({ 
              label, 
              value 
            }))}
          />
        </div>

        <div style={{ marginBottom: 16 }}>
          <Text strong>专词映射表</Text>
          <Select
            style={{ width: '100%', marginTop: 8 }}
            placeholder="选择专词映射表"
            value={dictionaryId}
            onChange={setDictionaryId}
            options={dictionaries.map(dict => ({ label: dict, value: dict }))}
          />
        </div>

        <div style={{ marginBottom: 16 }}>
          <Text strong>翻译模型</Text>
          <Select
            style={{ width: '100%', marginTop: 8 }}
            placeholder="翻译模型"
            value={modelId}
            onChange={setModelId}
            options={models.map(model => ({ label: model, value: model }))}
          />
        </div>

        <div style={{ marginBottom: 16 }}>
          <Text strong>并发数量</Text>
          <Slider
            min={1}
            max={10}
            value={concurrency}
            onChange={setConcurrency}
            marks={{
              1: '1',
              5: '5',
              10: '10'
            }}
          />
        </div>

        <div style={{ marginBottom: 24 }}>
          <Text strong>环境</Text>
          <Select
            style={{ width: '100%', marginTop: 8 }}
            placeholder="Lambda 别名"
            value={lambdaAlias}
            onChange={setLambdaAlias}
            options={[
              { label: '测试环境', value: 'staging' },
              { label: '生产环境', value: 'prod' }
            ]}
          />
        </div>

        <Button 
          type="primary" 
          onClick={handleTranslate} 
          loading={fileTranslationLoading}
          disabled={!file}
          block
        >
          翻译文件
        </Button>

        {fileTranslationLoading && (
          <div style={{ textAlign: 'center', marginTop: 24 }}>
            <Spin />
            <Text style={{ display: 'block', marginTop: 8 }}>
              正在处理文件，请稍候...
            </Text>
            <Text type="secondary" style={{ display: 'block', marginTop: 4 }}>
              处理完成后，文件将自动下载
            </Text>
          </div>
        )}
      </Card>
    </div>
  );
};

export default ExcelTranslatePage;
