import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { orchestrationId, hostUrl, agentId } = await request.json();

    // Generate a simple session ID using timestamp and random number
    const sessionId = `session-${Date.now()}-${Math.random().toString(36).substring(7)}`;
    
    return NextResponse.json({
      sessionId,
      success: true,
    });
  } catch (error) {
    console.error('Error initializing chat session:', error);
    const fallbackSessionId = `session-${Date.now()}-${Math.random().toString(36).substring(7)}`;
    return NextResponse.json(
      { error: 'Failed to initialize chat session', sessionId: fallbackSessionId },
      { status: 200 } // Return 200 with a generated session ID as fallback
    );
  }
}

// Made with Bob
