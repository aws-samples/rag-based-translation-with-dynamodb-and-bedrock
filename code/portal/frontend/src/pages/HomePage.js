import React, { useEffect, useState } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Select, 
  Button, 
  Input, 
  Spin, 
  Alert, 
  Typography,
  Divider,
  Form
} from 'antd';
import { useDispatch, useSelector } from 'react-redux';

import { 
  translateText, 
  fetchModels, 
  fetchLanguages, 
  fetchDictionaries,
  clearTranslation,
  clearError
} from '../store/slices/translationSlice';

const { TextArea } = Input;
const { Title } = Typography;

const HomePage = () => {
  const dispatch = useDispatch();
  const { 
    translatedText, 
    termMapping, 
    models, 
    languages, 
    dictionaries, 
    loading, 
    error 
  } = useSelector((state) => state.translation);

  const [inputText, setInputText] = useState('');
  const [sourceLang, setSourceLang] = useState('');
  const [targetLang, setTargetLang] = useState('');
  const [modelId, setModelId] = useState('');
  const [dictionaryId, setDictionaryId] = useState('');
  const [lambdaAlias, setLambdaAlias] = useState('staging');

  useEffect(() => {
    dispatch(fetchModels());
    dispatch(fetchLanguages());
    dispatch(fetchDictionaries());

    return () => {
      dispatch(clearTranslation());
      dispatch(clearError());
    };
  }, [dispatch]);

  useEffect(() => {
    if (languages && Object.keys(languages).length > 0) {
      const langKeys = Object.keys(languages);
      setSourceLang(languages[langKeys[0]]);
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

  const handleTranslate = () => {
    if (!inputText.trim()) return;

    dispatch(translateText({
      contents: [inputText],
      source_lang: sourceLang,
      target_lang: targetLang,
      dictionary_id: dictionaryId,
      model_id: modelId,
      lambda_alias: lambdaAlias
    }));
  };

  return (
    <div className="translation-container">
      <Title level={2}>LLM 翻译工具</Title>
      
      {error && (
        <Alert
          message="翻译错误"
          description={error}
          type="error"
          showIcon
          closable
          onClose={() => dispatch(clearError())}
          style={{ marginBottom: 16 }}
        />
      )}

      <Card>
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Form.Item label="专词映射表" style={{ marginBottom: 16 }}>
              <Select
                style={{ width: '100%' }}
                placeholder="选择专词映射表"
                value={dictionaryId}
                onChange={setDictionaryId}
                options={dictionaries.map(dict => ({ label: dict, value: dict }))}
              />
            </Form.Item>
            <Form.Item label="源语言" style={{ marginBottom: 16 }}>
              <Select
                style={{ width: '100%' }}
                placeholder="源语言"
                value={sourceLang}
                onChange={setSourceLang}
                options={Object.entries(languages).map(([label, value]) => ({ 
                  label, 
                  value 
                }))}
              />
            </Form.Item>
            <TextArea
              placeholder="请在此输入要翻译的文本"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              rows={10}
              style={{ marginBottom: 16 }}
            />
          </Col>
          <Col span={12}>
            <Form.Item label="翻译模型" style={{ marginBottom: 16 }}>
              <Select
                style={{ width: '100%' }}
                placeholder="翻译模型"
                value={modelId}
                onChange={setModelId}
                options={models.map(model => ({ label: model, value: model }))}
              />
            </Form.Item>
            <Form.Item label="目标语言" style={{ marginBottom: 16 }}>
              <Select
                style={{ width: '100%' }}
                placeholder="目标语言"
                value={targetLang}
                onChange={setTargetLang}
                options={Object.entries(languages).map(([label, value]) => ({ 
                  label, 
                  value 
                }))}
              />
            </Form.Item>
            <TextArea
              placeholder="翻译后的文本"
              value={translatedText}
              rows={10}
              readOnly
              style={{ marginBottom: 16 }}
            />
          </Col>
        </Row>

        <Row>
          <Col span={24}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Form.Item label="环境" style={{ marginBottom: 0 }}>
                <Select
                  style={{ width: 120 }}
                  placeholder="Lambda 别名"
                  value={lambdaAlias}
                  onChange={setLambdaAlias}
                  options={[
                    { label: '测试环境', value: 'staging' },
                    { label: '生产环境', value: 'prod' }
                  ]}
                />
              </Form.Item>
              <Button 
                type="primary" 
                onClick={handleTranslate} 
                loading={loading}
                disabled={!inputText.trim()}
              >
                开始翻译
              </Button>
            </div>
          </Col>
        </Row>

        <Divider>专词映射关系</Divider>
        <Card 
          title="召回的专词映射" 
          bordered={true} 
          style={{ marginBottom: '16px' }}
        >
          {termMapping ? (
            <TextArea
              value={termMapping}
              rows={8}
              readOnly
              style={{ backgroundColor: '#f5f5f5' }}
            />
          ) : (
            <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
              翻译后将在此处显示专词映射关系
            </div>
          )}
        </Card>
      </Card>
    </div>
  );
};

export default HomePage;
