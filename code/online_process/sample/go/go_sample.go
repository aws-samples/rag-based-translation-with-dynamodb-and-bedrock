package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/lambda"
)

// AWS and model configuration
const (
	region             = "us-west-2"
	modelID            = "anthropic.claude-3-haiku-20240307-v1:0"
	dictionaryID       = "test_dict1"
	sourceLang         = "CHS"
	targetLang         = "EN"
	lambdaFunctionName = "translate_tool"
)

// Payload represents the structure of the Lambda function payload
type Payload struct {
	SrcContent   string `json:"src_content"`
	SrcLang      string `json:"src_lang"`
	DestLang     string `json:"dest_lang"`
	RequestType  string `json:"request_type"`
	DictionaryID string `json:"dictionary_id"`
	ModelID      string `json:"model_id"`
}

// Response represents the structure of the Lambda function response
type Response struct {
	Result      string        `json:"result"`
	TermMapping []interface{} `json:"term_mapping"` // Changed to []interface{}
}

// createLambdaClient creates and returns an AWS Lambda client
func createLambdaClient(ctx context.Context) (*lambda.Client, error) {
	cfg, err := config.LoadDefaultConfig(ctx, config.WithRegion(region))
	if err != nil {
		return nil, fmt.Errorf("failed to load AWS configuration: %v", err)
	}
	return lambda.NewFromConfig(cfg), nil
}

// createPayload creates the payload for the Lambda function
func createPayload(content, srcLang, destLang, dictionaryID, modelID string) Payload {
	return Payload{
		SrcContent:   content,
		SrcLang:      srcLang,
		DestLang:     destLang,
		RequestType:  "translate",
		DictionaryID: dictionaryID,
		ModelID:      modelID,
	}
}

// invokeLambdaFunction invokes the Lambda function and returns the response
func invokeLambdaFunction(ctx context.Context, client *lambda.Client, functionName string, payload Payload) (*Response, error) {
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal payload: %v", err)
	}

	input := &lambda.InvokeInput{
		FunctionName: aws.String(functionName),
		Payload:      payloadBytes,
	}

	result, err := client.Invoke(ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to invoke Lambda function: %v", err)
	}

	var response Response
	err = json.Unmarshal(result.Payload, &response)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %v", err)
	}

	return &response, nil
}

func main() {
	ctx := context.Background()

	// Initialize Lambda client
	lambdaClient, err := createLambdaClient(ctx)
	if err != nil {
		log.Fatalf("Failed to create Lambda client: %v", err)
	}

	// Content to be translated
	content := "蚕食者之影在哪里能找到？"
	fmt.Printf("Original content: %s\n", content)

	// Create payload for Lambda function
	payload := createPayload(content, sourceLang, targetLang, dictionaryID, modelID)

	// Invoke Lambda function
	response, err := invokeLambdaFunction(ctx, lambdaClient, lambdaFunctionName, payload)
	if err != nil {
		log.Fatalf("Failed to invoke Lambda function: %v", err)
	}

	// Print results
	fmt.Printf("Translated result: %s\n", response.Result)
	fmt.Printf("Term mapping: %v\n", response.TermMapping)
}
