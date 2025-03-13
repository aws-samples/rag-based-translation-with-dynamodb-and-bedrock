import React, { useEffect, useState } from 'react';
import { 
  Card, 
  Tabs, 
  Upload, 
  Button, 
  Input, 
  Select, 
  Typography, 
  Alert, 
  Spin,
  Form,
  Checkbox,
  Space,
  message,
  Modal,
  Divider,
  Tag,
  Row,
  Col
} from 'antd';
import { UploadOutlined, SearchOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';

import { 
  fetchDictionaries,
  fetchDictionaryVersions,
  fetchDictionaryTerm,
  updateDictionaryTerm,
  updateDictionaryVersion,
  uploadDictionary,
  checkDictionaryJobStatus,
  checkDictionaryQuality,
  clearCurrentTerm,
  clearError,
  clearUploadSuccess,
  clearQualityCheckResult,
  clearJobStatus
} from '../store/slices/dictionarySlice';

const { Title, Text, Paragraph } = Typography;
const { TabPane } = Tabs;
const { TextArea } = Input;

const DictionaryManagementPage = () => {
  // Helper function to get the next version number
  const getNextVersion = (dictionaryName) => {
    if (!dictionaryVersions[dictionaryName] || dictionaryVersions[dictionaryName].length === 0) {
      return 'v1';
    }
    
    // Find the highest version number
    const versions = dictionaryVersions[dictionaryName]
      .filter(v => v.startsWith('v'))
      .map(v => parseInt(v.substring(1), 10))
      .filter(v => !isNaN(v));
    
    if (versions.length === 0) {
      return 'v1';
    }
    
    const maxVersion = Math.max(...versions);
    return `v${maxVersion + 1}`;
  };
  const dispatch = useDispatch();
  const { 
    dictionaries,
    dictionaryVersions,
    currentTerm,
    loading,
    error,
    uploadLoading,
    uploadError,
    uploadSuccess,
    jobStatus,
    qualityCheckResult
  } = useSelector((state) => state.dictionary);

  // Tab 1: Upload Dictionary
  const [uploadFile, setUploadFile] = useState(null);
  const [createNew, setCreateNew] = useState(false);
  const [selectedDictionary, setSelectedDictionary] = useState('');
  const [newDictionaryName, setNewDictionaryName] = useState('');
  const [selectedVersion, setSelectedVersion] = useState('');

  // Tab 2: Version Management
  const [versionDictionary, setVersionDictionary] = useState('');
  const [versionToUpdate, setVersionToUpdate] = useState('');
  
  // Tab 3: Search Terms
  const [searchDictionary, setSearchDictionary] = useState('');
  const [searchVersion, setSearchVersion] = useState('default');
  const [searchTerm, setSearchTerm] = useState('');
  const [editedTerm, setEditedTerm] = useState(null);

  // Job status polling
  const [polling, setPolling] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    dispatch(fetchDictionaries());
    dispatch(fetchDictionaryVersions());

    return () => {
      dispatch(clearCurrentTerm());
      dispatch(clearError());
      dispatch(clearUploadSuccess());
      dispatch(clearQualityCheckResult());
    };
  }, [dispatch]);

  useEffect(() => {
    if (dictionaries.length > 0) {
      setSelectedDictionary(dictionaries[0]);
      setVersionDictionary(dictionaries[0]);
      setSearchDictionary(dictionaries[0]);
    }
  }, [dictionaries]);

  useEffect(() => {
    if (dictionaryVersions[versionDictionary]?.length > 0) {
      setVersionToUpdate(dictionaryVersions[versionDictionary][0]);
    }
  }, [versionDictionary, dictionaryVersions]);

  useEffect(() => {
    if (dictionaryVersions[searchDictionary]?.length > 0) {
      setSearchVersion('default');
    }
  }, [searchDictionary, dictionaryVersions]);

  // Poll job status
  useEffect(() => {
    let statusInterval;
    if (polling && jobStatus?.runId) {
      statusInterval = setInterval(() => {
        // Check job status
        dispatch(checkDictionaryJobStatus(jobStatus.runId));
      }, 2000);
    }
    
    return () => {
      if (statusInterval) clearInterval(statusInterval);
    };
  }, [polling, jobStatus?.runId, dispatch]);

  // Update elapsed time
  useEffect(() => {
    let timeInterval;
    if (polling) {
      // Reset elapsed time when starting to poll
      setElapsedTime(0);
      
      // Update elapsed time every second
      timeInterval = setInterval(() => {
        setElapsedTime(prevTime => prevTime + 1);
      }, 1000);
    } else {
      // Reset elapsed time when polling stops
      setElapsedTime(0);
    }
    
    return () => {
      if (timeInterval) clearInterval(timeInterval);
    };
  }, [polling]);

  // Handle job status changes
  useEffect(() => {
    if (jobStatus?.status === 'SUCCEEDED' || 
        jobStatus?.status === 'FAILED' || 
        jobStatus?.status === 'TIMEOUT') {
      
      // Stop polling when job is completed
      setPolling(false);
      
      // Show notification and update data if needed
      if (jobStatus.status === 'SUCCEEDED') {
        message.success('字典处理成功');
        dispatch(fetchDictionaries());
        dispatch(fetchDictionaryVersions());
      } else if (jobStatus.status === 'FAILED' || jobStatus.status === 'TIMEOUT') {
        message.error(`字典处理失败: ${jobStatus.status}`);
      }
    }
  }, [jobStatus?.status, dispatch]);

  // Start polling when upload is successful and job is not completed
  useEffect(() => {
    if (uploadSuccess && jobStatus?.runId) {
      const isCompleted = ['SUCCEEDED', 'FAILED', 'TIMEOUT'].includes(jobStatus.status);
      if (!isCompleted) {
        setPolling(true);
      }
    }
  }, [uploadSuccess, jobStatus]);

  // Handle file upload
  const handleFileChange = (info) => {
    if (info.file.status === 'done') {
      message.success(`${info.file.name} 上传成功`);
      setUploadFile(info.file.originFileObj);
      
      // Clear previous job status when a new file is selected
      if (jobStatus) {
        dispatch(clearJobStatus());
      }
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} 上传失败`);
    }
  };

  // Handle dictionary upload
  const handleUploadDictionary = () => {
    if (!uploadFile) {
      message.warning('请先上传JSON文件');
      return;
    }

    const dictionaryName = createNew ? newDictionaryName : selectedDictionary;
    if (!dictionaryName) {
      message.warning('请选择或输入字典名称');
      return;
    }

    // Clear previous job status before starting a new upload
    if (jobStatus) {
      dispatch(clearJobStatus());
    }

    // Clear previous quality check result before starting a new upload
    if (qualityCheckResult) {
      dispatch(clearQualityCheckResult());
    }

    // If updating an existing dictionary, use the next version
    const version = !createNew ? getNextVersion(selectedDictionary) : undefined;
    
    dispatch(uploadDictionary({
      file: uploadFile,
      dictionaryName,
      isNew: createNew,
      version: version
    }));
  };

  // Handle quality check
  const handleQualityCheck = () => {
    if (!uploadFile) {
      message.warning('请先上传JSON文件');
      return;
    }

    dispatch(checkDictionaryQuality(uploadFile));
  };

  // Handle version update
  const handleUpdateVersion = () => {
    if (!versionDictionary || !versionToUpdate) {
      message.warning('请选择字典和版本');
      return;
    }

    dispatch(updateDictionaryVersion({
      dictId: versionDictionary,
      version: versionToUpdate
    }));
    
    message.success(`已更新 ${versionDictionary} 的版本为 ${versionToUpdate}`);
  };

  // Handle term search
  const handleSearchTerm = () => {
    if (!searchTerm.trim()) {
      message.warning('请输入要搜索的专词');
      return;
    }

    let dictName = searchDictionary;
    if (searchVersion !== 'default') {
      dictName = `${searchDictionary}_${searchVersion}`;
    }

    dispatch(fetchDictionaryTerm({
      dictionaryName: dictName,
      term: searchTerm.trim()
    }));
  };

  // Handle term update
  const handleUpdateTerm = () => {
    if (!editedTerm) {
      message.warning('请先编辑专词');
      return;
    }

    let dictName = searchDictionary;
    if (searchVersion !== 'default') {
      dictName = `${searchDictionary}_${searchVersion}`;
    }

    dispatch(updateDictionaryTerm({
      dictionaryName: dictName,
      term: editedTerm.term,
      termData: {
        entity: editedTerm.entity,
        mapping: editedTerm.mapping
      }
    }));

    message.success('专词更新成功');
  };

  // Handle JSON edit
  const handleJsonEdit = (value) => {
    try {
      const parsed = JSON.parse(value);
      setEditedTerm(parsed);
    } catch (e) {
      message.error('JSON格式错误');
    }
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    accept: '.json',
    maxCount: 1,
    beforeUpload: (file) => {
      const isJson = file.type === 'application/json';
      if (!isJson) {
        message.error('只能上传JSON文件!');
      }
      return isJson ? true : Upload.LIST_IGNORE;
    },
    customRequest: ({ file, onSuccess }) => {
      setTimeout(() => {
        onSuccess('ok');
      }, 0);
    },
    onChange: handleFileChange,
  };

  return (
    <div className="dictionary-container">
      <Title level={2}>专词映射表配置</Title>
      
      {error && (
        <Alert
          message="操作错误"
          description={error}
          type="error"
          showIcon
          closable
          onClose={() => dispatch(clearError())}
          style={{ marginBottom: 16 }}
        />
      )}

      <Card>
        <Tabs defaultActiveKey="1">
          <TabPane tab="创建/更新专词映射表" key="1">
            <div className="file-upload-container">
              <Upload {...uploadProps}>
                <Button icon={<UploadOutlined />}>选择JSON文件</Button>
              </Upload>
              <Text type="secondary" style={{ display: 'block', marginTop: 8 }}>
                支持 .json 格式
              </Text>
            </div>

            <Divider />

            <Form layout="vertical">
              <Form.Item>
                <Checkbox 
                  checked={createNew} 
                  onChange={(e) => setCreateNew(e.target.checked)}
                >
                  创建新的专词映射表
                </Checkbox>
              </Form.Item>

              {createNew ? (
                <Form.Item 
                  label="新专词映射表名称" 
                  validateStatus={newDictionaryName.includes(' ') ? 'error' : ''}
                  help={newDictionaryName.includes(' ') ? '映射字典名称不能存在空格' : ''}
                >
                  <Input 
                    value={newDictionaryName} 
                    onChange={(e) => setNewDictionaryName(e.target.value)}
                    placeholder="输入新专词映射表名称"
                  />
                </Form.Item>
              ) : (
                <>
                  <Form.Item label="选择现有专词映射表">
                    <Select
                      style={{ width: '100%' }}
                      value={selectedDictionary}
                      onChange={setSelectedDictionary}
                      options={dictionaries.map(dict => ({ label: dict, value: dict }))}
                    />
                  </Form.Item>

                  <Paragraph>
                    字典 {selectedDictionary} 存在如下版本:
                    <div style={{ marginTop: 8 }}>
                      {dictionaryVersions[selectedDictionary]?.map(v => (
                        <Tag key={v} color="blue" style={{ marginRight: 8 }}>{v}</Tag>
                      ))}
                    </div>
                  </Paragraph>
                  
                  <Paragraph>
                    将自动创建新版本: {getNextVersion(selectedDictionary)}
                  </Paragraph>
                </>
              )}

              <Space style={{ marginTop: 16 }}>
                <Button 
                  type="primary" 
                  onClick={handleUploadDictionary}
                  loading={uploadLoading}
                  disabled={!uploadFile || (createNew && !newDictionaryName)}
                >
                  上传
                </Button>
                <Button 
                  onClick={handleQualityCheck}
                  disabled={!uploadFile}
                >
                  质量检查
                </Button>
              </Space>
            </Form>

            {jobStatus && (
              <Alert
                message={jobStatus.status === 'SUCCEEDED' ? "上传成功" : "处理中"}
                description={
                  <div>
                    <p>字典已上传并{jobStatus.status === 'SUCCEEDED' ? '处理完成' : '开始处理'}。</p>
                    <p>
                      处理状态: {jobStatus.status} 
                      {polling && <Spin size="small" style={{ marginLeft: 8 }} />}
                    </p>
                    {polling && (
                      <p>已运行时间: {
                        elapsedTime < 60 
                          ? `${elapsedTime} 秒` 
                          : `${Math.floor(elapsedTime / 60)} 分 ${elapsedTime % 60} 秒`
                      }</p>
                    )}
                    {jobStatus.status === 'SUCCEEDED' && (
                      <p style={{ color: '#52c41a' }}>
                        <CheckCircleOutlined /> 字典处理已完成，可以使用了
                      </p>
                    )}
                    {jobStatus.status === 'FAILED' && (
                      <p style={{ color: '#f5222d' }}>
                        <CloseCircleOutlined /> 字典处理失败，请检查日志
                      </p>
                    )}
                  </div>
                }
                type={
                  jobStatus.status === 'SUCCEEDED' ? "success" : 
                  jobStatus.status === 'FAILED' || jobStatus.status === 'TIMEOUT' ? "error" : 
                  "info"
                }
                showIcon
                style={{ marginTop: 16 }}
              />
            )}

            {qualityCheckResult && (
              <div style={{ marginTop: 16 }}>
                <Alert
                  message="质量检查结果"
                  description={
                    <div>
                      <p>
                        <Text type={qualityCheckResult.errors > 0 ? 'danger' : 'success'}>
                          错误: {qualityCheckResult.errors}
                        </Text>
                      </p>
                      <p>
                        <Text type={qualityCheckResult.warnings > 0 ? 'warning' : 'success'}>
                          警告: {qualityCheckResult.warnings}
                        </Text>
                      </p>
                      {qualityCheckResult.errors > 0 && (
                        <div>
                          <Text type="danger">存在错误，无法上传</Text>
                        </div>
                      )}
                    </div>
                  }
                  type={qualityCheckResult.errors > 0 ? 'error' : 'success'}
                  showIcon
                />
              </div>
            )}
          </TabPane>

          <TabPane tab="专词映射表版本管理" key="2">
            <Form layout="vertical">
              <Form.Item label="选择专词映射表">
                <Select
                  style={{ width: '100%' }}
                  value={versionDictionary}
                  onChange={setVersionDictionary}
                  options={dictionaries.map(dict => ({ label: dict, value: dict }))}
                />
              </Form.Item>

              {dictionaryVersions[versionDictionary]?.length <= 1 ? (
                <Alert
                  message={`字典 ${versionDictionary} 只有默认版本`}
                  type="warning"
                  showIcon
                />
              ) : (
                <>
                  <Paragraph>
                    字典 {versionDictionary} 存在如下版本:
                    <div style={{ marginTop: 8 }}>
                      {dictionaryVersions[versionDictionary]?.map(v => (
                        <Tag key={v} color="blue" style={{ marginRight: 8 }}>{v}</Tag>
                      ))}
                    </div>
                  </Paragraph>

                  <Form.Item label="选择要设置的版本">
                    <Select
                      style={{ width: '100%' }}
                      value={versionToUpdate}
                      onChange={setVersionToUpdate}
                      options={dictionaryVersions[versionDictionary]?.map(v => ({ 
                        label: v, 
                        value: v 
                      }))}
                    />
                  </Form.Item>

                  <Button 
                    type="primary" 
                    onClick={handleUpdateVersion}
                  >
                    修改
                  </Button>
                </>
              )}
            </Form>
          </TabPane>

          <TabPane tab="专词映射表内容搜索" key="3">
            <Form layout="vertical">
              <Form.Item label="选择专词映射表">
                <Select
                  style={{ width: '100%' }}
                  value={searchDictionary}
                  onChange={setSearchDictionary}
                  options={dictionaries.map(dict => ({ label: dict, value: dict }))}
                />
              </Form.Item>

              {dictionaryVersions[searchDictionary]?.length > 1 && (
                <Form.Item label="选择版本">
                  <Select
                    style={{ width: '100%' }}
                    value={searchVersion}
                    onChange={setSearchVersion}
                    options={dictionaryVersions[searchDictionary]?.map(v => ({ 
                      label: v, 
                      value: v 
                    }))}
                  />
                </Form.Item>
              )}

              <Form.Item label="专词搜索">
                <Input
                  placeholder="输入要搜索的专词"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  suffix={
                    <Button 
                      type="text" 
                      icon={<SearchOutlined />} 
                      onClick={handleSearchTerm}
                    />
                  }
                  onPressEnter={handleSearchTerm}
                />
              </Form.Item>
            </Form>

            {loading && <Spin style={{ display: 'block', margin: '20px auto' }} />}

            {currentTerm && (
              <div className="term-editor">
                <Divider>搜索结果</Divider>
                
                <div>
                  <Title level={5}>专词详情</Title>
                  <pre style={{ 
                    background: '#f5f5f5', 
                    padding: 16, 
                    borderRadius: 4,
                    maxHeight: 600,
                    overflow: 'auto'
                  }}>
                    {JSON.stringify(currentTerm, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default DictionaryManagementPage;
