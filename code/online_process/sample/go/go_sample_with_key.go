package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/lambda"
)

// Configuration constants
const (
	Region             = "ap-southeast-1"
	ModelID            = "anthropic.claude-3-haiku-20240307-v1:0"
	DictionaryID       = "dict_1"
	SourceLang         = "en-us"
	TargetLang         = "zh-cn"
	LambdaFunctionName = "translate_tool"
	AK                 = "XXXX"
	SK                 = "YYYYY"
)

// createLambdaClient creates and returns an AWS Lambda client
func createLambdaClient(region, ak, sk string) *lambda.Lambda {
	sess, err := session.NewSession(&aws.Config{
		Region:      aws.String(region),
		Credentials: credentials.NewStaticCredentials(ak, sk, ""),
	})
	if err != nil {
		log.Fatalf("Failed to create session: %v", err)
	}
	return lambda.New(sess)
}

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
func invokeLambdaFunction(client *lambda.Lambda, functionName string, payload Payload) (map[string]interface{}, error) {
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("error marshalling payload: %v", err)
	}

	input := &lambda.InvokeInput{
		FunctionName: aws.String(functionName),
		Payload:      payloadBytes,
	}

	result, err := client.Invoke(input)
	if err != nil {
		return nil, fmt.Errorf("error invoking Lambda function: %v", err)
	}

	var response map[string]interface{}
	err = json.Unmarshal(result.Payload, &response)
	if err != nil {
		return nil, fmt.Errorf("error unmarshalling response: %v", err)
	}

	return response, nil
}

func main() {
	// Initialize Lambda client
	lambdaClient := createLambdaClient(Region, AK, SK)

	// Content to be translated
	contents := []string{"miHoYo is great!"}
	fmt.Printf("Original contents: %v\n", contents)
	fmt.Println("--------------------")

	// Create payload for Lambda function
	payload := createPayload(contents, SourceLang, TargetLang, dictionaryID, ModelID, false)

	fmt.Printf("input: %+v\n", payload)

	// Invoke Lambda function
	response, err := invokeLambdaFunction(lambdaClient, LambdaFunctionName, payload)
	if err != nil {
		log.Fatalf("Failed to invoke Lambda function: %v", err)
	}
	fmt.Printf("response: %+v\n", response)

	// Extract results
	translations, ok := response["translations"].([]interface{})
	if !ok {
		log.Fatal("Failed to parse translations from response")
	}

	for _, trans := range translations {
		translation, ok := trans.(map[string]interface{})
		if !ok {
			continue
		}

		if termMapping, ok := translation["term_mapping"].([]interface{}); ok {
			for _, mapping := range termMapping {
				if m, ok := mapping.([]interface{}); ok && len(m) == 3 {
					fmt.Printf("Origin Term: %v, Translated: %v, Entity: %v\n", m[0], m[1], m[2])
				}
			}
		}

		if translatedText, ok := translation["translated_text"].(string); ok {
			fmt.Printf("Translated Text: %s\n", translatedText)
		}

		if model, ok := translation["model"].(string); ok {
			fmt.Printf("Model: %s\n", model)
		}

		if glossaryConfig, ok := translation["glossary_config"].(string); ok {
			fmt.Printf("Dict: %s\n", glossaryConfig)
		}

		fmt.Println("--------------------")
	}
}
