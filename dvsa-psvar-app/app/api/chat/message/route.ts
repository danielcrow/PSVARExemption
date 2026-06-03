import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { sessionId, message, orchestrationId, hostUrl, agentId } = await request.json();

    // Use the watsonx Orchestrate chat API endpoint
    // The correct endpoint format is: {hostURL}/wxochat/api/v1/chat
    const chatUrl = `${hostUrl}/wxochat/api/v1/chat`;
    
    const response = await fetch(chatUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        orchestrationID: orchestrationId,
        agentId: agentId,
        sessionId: sessionId,
        message: message,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Chat API error (${response.status}):`, errorText);
      throw new Error(`Failed to send message: ${response.statusText}`);
    }

    const data = await response.json();
    
    // Extract the assistant's response from the watsonx Orchestrate response
    let responseText = 'I apologize, but I encountered an error processing your request.';
    
    if (data.response) {
      responseText = data.response;
    } else if (data.message) {
      responseText = data.message;
    } else if (data.text) {
      responseText = data.text;
    }

    return NextResponse.json({
      response: responseText,
      raw: data, // Include raw response for debugging
    });
  } catch (error) {
    console.error('Error sending message:', error);
    return NextResponse.json(
      { 
        error: 'Failed to send message', 
        response: 'I apologize, but I encountered an error. Please try again.',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 200 } // Return 200 to prevent UI errors
    );
  }
}

// Made with Bob
