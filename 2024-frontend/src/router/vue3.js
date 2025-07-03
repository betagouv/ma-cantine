import authenticatedRoutes from "./authenticated-routes"
import publicRoutes from "./public-routes"

const vue3routes = [...authenticatedRoutes, ...publicRoutes]

export default vue3routes
