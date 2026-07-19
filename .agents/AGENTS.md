# Frontend Build Guidelines

Whenever the user asks you to build, test, or verify the frontend UI application, you MUST perform the following validation checklist:

1. **Prettier Code Formatting**:
   - Run `npm run format` to automatically format all files using Prettier.
2. **ESLint Static Analysis**:
   - Run `npm run lint` to verify ESLint compliance.
3. **Jest Unit & E2E Tests**:
   - Run `npm run test` to verify all frontend test suites pass successfully.
4. **Production Compilation**:
   - Run `npm run build` to verify the Next.js production build creates successfully and compiles without errors.

## Lessons Learned & Common Issues

- **API Proxy Response Envelope Unwrapping**:
  - The Next.js API routes (`src/app/api/admin/**/*.js`) proxy and unwrap the Spring Boot `ApiResponse` envelope (`responseData.data`).
  - Always use null-safe unwrapping logic to handle cases where the backend returns an explicit `null` payload:
    `const unwrappedData = responseData.data !== undefined && responseData.data !== null ? responseData.data : responseData;`
  - Always preserve response metadata (`success` and `message`) by copying them from the outer wrapper to the unwrapped object (if not already set) before returning the response. This is critical for authentication checks (`auth/route.js`).
- **Modal Contrast Styling (Light/Dark Themes)**:
  - Do not hardcode fixed light colors (like `text-slate-300`) for text items that will be rendered inside white or light-gray components in light mode.
  - Always wrap them with the theme helper `t('text-slate-300', 'text-slate-700')` to ensure clear legibility across both themes.
