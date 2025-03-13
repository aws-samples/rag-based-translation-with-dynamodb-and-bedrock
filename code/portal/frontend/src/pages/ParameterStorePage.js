import React, { useEffect, useState } from 'react';
import { 
  Card, 
  Input, 
  Button, 
  Typography, 
  Alert, 
  Spin,
  List,
  Divider,
  Modal,
  Form,
  message
} from 'antd';
import { EditOutlined, SaveOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';

import { 
  fetchParameters,
  updateParameter,
  clearError,
  clearUpdateSuccess
} from '../store/slices/parameterSlice';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;

const ParameterStorePage = () => {
  const dispatch = useDispatch();
  const { parameters, loading, error, updateSuccess } = useSelector((state) => state.parameter);

  const [path, setPath] = useState('/');
  const [editingParameter, setEditingParameter] = useState(null);
  const [editValue, setEditValue] = useState('');
  const [isModalVisible, setIsModalVisible] = useState(false);

  useEffect(() => {
    return () => {
      dispatch(clearError());
      dispatch(clearUpdateSuccess());
    };
  }, [dispatch]);

  useEffect(() => {
    if (updateSuccess) {
      message.success('参数更新成功');
      setIsModalVisible(false);
      dispatch(clearUpdateSuccess());
    }
  }, [updateSuccess, dispatch]);

  const handleFetchParameters = () => {
    dispatch(fetchParameters(path));
  };

  const handleEditParameter = (parameter) => {
    setEditingParameter(parameter);
    setEditValue(parameter.Value);
    setIsModalVisible(true);
  };

  const handleUpdateParameter = () => {
    dispatch(updateParameter({
      name: editingParameter.Name,
      value: editValue
    }));
  };

  const handleModalCancel = () => {
    setIsModalVisible(false);
    setEditingParameter(null);
    setEditValue('');
  };

  return (
    <div className="parameter-container">
      <Title level={2}>参数配置</Title>
      
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
        <Form layout="inline" style={{ marginBottom: 16 }}>
          <Form.Item label="参数路径" style={{ flex: 1 }}>
            <Input
              placeholder="输入参数路径，例如: /translate"
              value={path}
              onChange={(e) => setPath(e.target.value)}
              onPressEnter={handleFetchParameters}
            />
          </Form.Item>
          <Form.Item>
            <Button 
              type="primary" 
              onClick={handleFetchParameters}
              loading={loading}
            >
              获取参数
            </Button>
          </Form.Item>
        </Form>

        <Divider />

        {loading ? (
          <div style={{ textAlign: 'center', padding: 24 }}>
            <Spin size="large" />
          </div>
        ) : (
          <>
            {parameters.length === 0 ? (
              <Alert
                message="没有找到参数"
                description="请检查路径是否正确，或者尝试其他路径"
                type="info"
                showIcon
              />
            ) : (
              <List
                itemLayout="vertical"
                dataSource={parameters}
                renderItem={(parameter) => (
                  <List.Item
                    key={parameter.Name}
                    actions={[
                      <Button 
                        key="edit" 
                        type="text" 
                        icon={<EditOutlined />}
                        onClick={() => handleEditParameter(parameter)}
                      >
                        编辑
                      </Button>
                    ]}
                  >
                    <div className="parameter-item">
                      <Title level={5}>{parameter.Name}</Title>
                      <Paragraph type="secondary">
                        最后修改时间: {new Date(parameter.LastModifiedDate).toLocaleString()}
                      </Paragraph>
                      <div style={{ 
                        background: '#f5f5f5', 
                        padding: 16, 
                        borderRadius: 4,
                        maxHeight: 200,
                        overflow: 'auto'
                      }}>
                        <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
                          {parameter.Value}
                        </pre>
                      </div>
                    </div>
                  </List.Item>
                )}
              />
            )}
          </>
        )}
      </Card>

      <Modal
        title={`编辑参数: ${editingParameter?.Name}`}
        open={isModalVisible}
        onCancel={handleModalCancel}
        footer={[
          <Button key="cancel" onClick={handleModalCancel}>
            取消
          </Button>,
          <Button 
            key="submit" 
            type="primary" 
            icon={<SaveOutlined />}
            onClick={handleUpdateParameter}
            loading={loading}
          >
            保存
          </Button>
        ]}
        width={800}
      >
        <TextArea
          rows={10}
          value={editValue}
          onChange={(e) => setEditValue(e.target.value)}
        />
      </Modal>
    </div>
  );
};

export default ParameterStorePage;
