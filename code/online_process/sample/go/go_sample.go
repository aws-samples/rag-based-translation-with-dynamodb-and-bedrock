package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/lambda"
)

// Configuration constants
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
	SrcContents             []string `json:"src_contents"`
	SrcLang                 string   `json:"src_lang"`
	DestLang                string   `json:"dest_lang"`
	RequestType             string   `json:"request_type"`
	DictionaryID            string   `json:"dictionary_id"`
	ModelID                 string   `json:"model_id"`
	ResponseWithTermMapping bool     `json:"response_with_term_mapping"`
}

// Translation represents the structure of a single translation in the response
type Translation struct {
	TranslatedText string      `json:"translated_text"`
	Model          string      `json:"model"`
	GlossaryConfig interface{} `json:"glossary_config"` // Changed from string to interface{}
	TermMapping    [][]string  `json:"term_mapping"`
}

// Response represents the structure of the Lambda function response
type Response struct {
	Translations []Translation `json:"translations"`
}

// createLambdaClient creates and returns an AWS Lambda client
func createLambdaClient(region string) *lambda.Lambda {
	sess := session.Must(session.NewSession(&aws.Config{
		Region: aws.String(region),
	}))
	return lambda.New(sess)
}

// createPayload creates the payload for the Lambda function
func createPayload(contents []string, srcLang, destLang, dictionaryID, modelID string, responseWithTermMapping bool) Payload {
	return Payload{
		SrcContents:             contents,
		SrcLang:                 srcLang,
		DestLang:                destLang,
		RequestType:             "translate",
		DictionaryID:            dictionaryID,
		ModelID:                 modelID,
		ResponseWithTermMapping: responseWithTermMapping,
	}
}

// invokeLambdaFunction invokes the Lambda function and returns the response
func invokeLambdaFunction(client *lambda.Lambda, functionName string, payload Payload) (*Response, error) {
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("error marshaling payload: %v", err)
	}

	input := &lambda.InvokeInput{
		FunctionName: aws.String(functionName),
		Payload:      payloadBytes,
	}

	result, err := client.Invoke(input)
	if err != nil {
		return nil, fmt.Errorf("error invoking Lambda function: %v", err)
	}

	var response Response
	err = json.Unmarshal(result.Payload, &response)
	if err != nil {
		return nil, fmt.Errorf("error unmarshaling response: %v", err)
	}

	return &response, nil
}

func main() {
	// Initialize Lambda client
	lambdaClient := createLambdaClient(region)

	// Content to be translated
	contents := []string{"蚕食者之影在哪里能找到？", "蚕食者之影的弱点是什么？"}
	fmt.Printf("Original contents: %v\n", contents)
	fmt.Println("--------------------")

	// Create payload for Lambda function
	payload := createPayload(contents, sourceLang, targetLang, dictionaryID, modelID, false)

	// Invoke Lambda function
	response, err := invokeLambdaFunction(lambdaClient, lambdaFunctionName, payload)
	if err != nil {
		log.Fatalf("Error invoking Lambda function: %v", err)
	}

	// Extract results
	for _, translation := range response.Translations {
		if len(translation.TermMapping) > 0 {
			for _, mapping := range translation.TermMapping {
				fmt.Printf("Origin Term: %s, Translated: %s, Entity: %s\n", mapping[0], mapping[1], mapping[2])
			}
		}

		fmt.Printf("Translated Text: %s\n", translation.TranslatedText)
		fmt.Printf("Model: %s\n", translation.Model)

		// Print GlossaryConfig as JSON string
		glossaryConfigJSON, err := json.Marshal(translation.GlossaryConfig)
		if err != nil {
			fmt.Printf("Error marshaling GlossaryConfig: %v\n", err)
		} else {
			fmt.Printf("Dict: %s\n", string(glossaryConfigJSON))
		}

		fmt.Println("--------------------")
	}
}
