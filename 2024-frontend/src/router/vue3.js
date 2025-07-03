import privateRoutes from "./private-routes"
import publicRoutes from "./public-routes"

const vue3routes = [...privateRoutes, ...publicRoutes]

export default vue3routes
