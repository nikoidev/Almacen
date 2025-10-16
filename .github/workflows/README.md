# 🚀 CI/CD Workflows - SGA Pro

Este directorio contiene los workflows de GitHub Actions para automatizar las pruebas y validaciones del proyecto.

## 📋 Workflows Disponibles

### 1. Backend CI (`backend-ci.yml`)

**Ejecuta en**:
- Push a cualquier rama (solo si cambia `/backend/**`)
- Pull Request hacia `main`

**Jobs**:
- **Lint & Test**
  - ✅ Configuración de Python 3.13
  - ✅ PostgreSQL 15 como servicio
  - ✅ Linting con `flake8`
  - ✅ Formateo con `black`
  - ✅ Verificación de modelos SQLAlchemy
  - 🔄 Tests con `pytest` (cuando se implementen)

- **Security Check**
  - ✅ Escaneo de vulnerabilidades con `safety`
  - ✅ Verificación de dependencias

### 2. Frontend CI (`frontend-ci.yml`)

**Ejecuta en**:
- Push a cualquier rama (solo si cambia `/frontend/**`)
- Pull Request hacia `main`

**Jobs**:
- **Lint & Build**
  - ✅ Node.js 18
  - ✅ ESLint para calidad de código
  - ✅ TypeScript type checking
  - ✅ Build de Next.js (modo producción)
  - ✅ Análisis de tamaño del build

- **Tests**
  - 🔄 Tests con Jest (cuando se implementen)

## 🎯 Estado de los Workflows

Los badges se actualizarán automáticamente en el README principal.

## 📊 Cómo Ver los Resultados

1. Ve a la pestaña **Actions** en GitHub
2. Selecciona el workflow que quieres ver
3. Click en el commit específico para ver detalles
4. Revisa los logs de cada job

## 🔧 Configuración Local

Para replicar las validaciones localmente:

### Backend
```bash
cd backend
pipenv install --dev
pipenv run flake8 app/
pipenv run black --check app/
pipenv run pytest
```

### Frontend
```bash
cd frontend
npm install
npm run lint
npx tsc --noEmit
npm run build
```

## 🚨 Solución de Problemas

### Backend CI falla
- Verifica que las dependencias en `Pipfile` estén correctas
- Asegúrate de que los modelos SQLAlchemy sean válidos
- Revisa los logs de PostgreSQL en el workflow

### Frontend CI falla
- Verifica `package.json` y `package-lock.json`
- Ejecuta `npm run lint` localmente
- Revisa errores de TypeScript con `npx tsc --noEmit`

## 📝 Notas

- Los jobs con `continue-on-error: true` no fallarán el build completo
- Los workflows solo se ejecutan si hay cambios en sus respectivos directorios
- PostgreSQL se levanta automáticamente para los tests de backend

## 🔄 Mejoras Futuras

- [ ] Añadir cobertura de tests (coverage)
- [ ] Implementar deploy automático a staging
- [ ] Añadir tests E2E con Playwright
- [ ] Cache de dependencias más agresivo
- [ ] Notificaciones de Slack/Discord

