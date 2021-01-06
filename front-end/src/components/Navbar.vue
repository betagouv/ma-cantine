<template>
  <div id="navbar">
    <router-link to="/">
      <div id="home">
        <img src="@/assets/logo-ma-cantine.png">
        <div>Pour une alimentatation saine, de qualité et plus durable dans nos assiettes grâce à EGAlim</div>
      </div>
    </router-link>
    <a id="about" href="https://beta.gouv.fr/startups/egalim.html" target="_blank">A propos</a>
  </div>
</template>

<script>
export default {
  name: 'Navbar',
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
  text-decoration: none;
}

#navbar {
  display: flex;
  justify-content: space-between;
  padding: 0px 50px;
}

#home {
  text-align: left;
  width: 300px;
  font-size: 11px;
  font-weight: 600;
  line-height: 15px;
  text-decoration: none;
  color: rgba(0,0,0,0.83);;
}

#about {
  margin: auto 0;
  border-radius: 25px;
  padding: 15px;
  font-size: 17px;
  line-height: 20px;
  color: rgba(64, 64, 64, 0.85);
}

#about:hover {
  color: white;
  background-color: rgba(0,0,0,0.33);
}
</style>
