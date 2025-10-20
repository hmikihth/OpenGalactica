import { Route, Navigate } from 'react-router-dom';

export function protectedRoute(path, element, isAuthenticated) {

  return (
    <Route
      key={path}
      path={path}
      element={isAuthenticated ? element : <Navigate to="/portal/" replace />}
    />
  );
}

export default protectedRoute;