# Custom watsonx Orchestrate Chat Interface

This application uses a custom-built chat interface that communicates directly with the watsonx Orchestrate REST API, providing full control over the UI and preventing layout issues caused by the embedded widget.

## Architecture

### Components

1. **ChatInterface.tsx** - Main chat component
   - Manages message state and UI
   - Handles user input and message display
   - Implements auto-scrolling and loading states
   - DVSA-branded styling with GOV.UK design system

2. **API Routes**
   - `/api/chat/init` - Initializes a new chat session
   - `/api/chat/message` - Sends messages and receives responses

### Features

✅ **Full Layout Control** - No widget-induced spacing issues
✅ **DVSA Branding** - Consistent GOV.UK design system styling
✅ **Responsive Design** - Works on all screen sizes
✅ **Real-time Chat** - Smooth message flow with loading indicators
✅ **Session Management** - Maintains conversation context
✅ **Error Handling** - Graceful error messages

## Configuration

The chat interface is configured in `app/page.tsx`:

```typescript
<ChatInterface
  orchestrationId="20250430-1552-4383-00f2-8e9318aa2f1b_20250501-1821-5146-80d6-0ef0535f5342"
  hostUrl="https://eu-central-1.dl.watson-orchestrate.ibm.com"
  agentId="a48c5531-927d-423b-b3d6-c20a291ac99a"
/>
```

## API Integration

### Session Initialization

```typescript
POST /api/chat/init
{
  "orchestrationId": "...",
  "hostUrl": "...",
  "agentId": "..."
}

Response:
{
  "sessionId": "session-123456789"
}
```

### Sending Messages

```typescript
POST /api/chat/message
{
  "sessionId": "session-123456789",
  "message": "User message here",
  "orchestrationId": "...",
  "hostUrl": "...",
  "agentId": "..."
}

Response:
{
  "response": "Assistant response here",
  "raw": { /* Full API response */ }
}
```

## Styling

The chat interface uses:
- **GOV.UK Design System** colors and typography
- **DVSA branding** (blue header, green buttons)
- **Smooth animations** for message appearance
- **Loading indicators** with animated dots
- **Custom scrollbar** styling

### Color Palette

- Primary Blue: `#1d70b8` (user messages)
- Success Green: `#00703c` (send button)
- Dark Grey: `#0b0c0c` (text)
- Light Grey: `#f3f2f1` (background)
- Border Grey: `#b1b4b6`

## Development

### Running Locally

```bash
cd dvsa-psvar-app
npm install
npm run dev
```

Open http://localhost:3000

### Building for Production

```bash
npm run build
npm start
```

### Deploying to Vercel

```bash
vercel deploy
```

## Troubleshooting

### Chat Not Loading

1. Check browser console for errors
2. Verify API credentials in `page.tsx`
3. Ensure watsonx Orchestrate endpoint is accessible

### Messages Not Sending

1. Check Network tab in browser DevTools
2. Verify session initialization succeeded
3. Check API route logs for errors

### Styling Issues

1. Clear browser cache
2. Check CSS module imports
3. Verify globals.css is loaded

## Future Enhancements

- [ ] File upload support
- [ ] Message history persistence
- [ ] Typing indicators
- [ ] Message timestamps
- [ ] Export conversation
- [ ] Multi-language support

## Support

For issues or questions:
- Email: enquiries@dvsa.gov.uk
- Phone: 0300 123 9000

---

Built with ❤️ using Next.js 14 and watsonx Orchestrate