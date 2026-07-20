import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
    const app = await NestFactory.create(AppModule);

    // Enable CORS for all origins and methods
    app.enableCors();

    // Configure Swagger documentation
    const config = new DocumentBuilder()
        .setTitle('BotanixUI API')
        .setDescription('Documentation for BotanixUI API services')
        .setVersion('1.0')
        .build();
    const document = SwaggerModule.createDocument(app, config);
    SwaggerModule.setup('api', app, document);

    // Start the application
    await app.listen(3000);
}

bootstrap();

This `index.ts` file serves as the main entry point for your BotanixUI API services. It sets up a NestJS application and initializes the Swagger documentation to provide API documentation.

### Explanation:
- **NestFactory.create(AppModule)**: Creates an instance of the NestJS application using the AppModule.
- **app.enableCors()**: Enables Cross-Origin Resource Sharing (CORS) globally for all origins, allowing requests from any domain.
- **DocumentBuilder and SwaggerModule**: Configures and sets up API documentation via Swagger.
- **SwaggerModule.setup('api', app, document)**: Sets up the Swagger UI at `/api` endpoint.

### Dependencies:
Ensure you have the following dependencies installed in your `package.json`:
{
  "dependencies": {
    "@nestjs/core": "^8.0.0",
    "@nestjs/swagger": "^6.1.0",
    "swagger-ui-express": "^4.5.7"
  }
}

### Note:
- Replace the placeholders in the Swagger documentation with actual details relevant to your project.
- Ensure that `AppModule` is correctly defined and contains all necessary modules, providers, and controllers for your API services.

This setup provides a robust starting point for your BotanixUI API layer.