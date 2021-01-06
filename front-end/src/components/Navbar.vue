<template>
  <div id="navbar">
    <router-link :to="{ name: 'landing' }" id="landing">
      <img src="@/assets/Marianne.png" id="Marianne">
      <div id="logo">
        <div id="ma-cantine-beta-gouv"><span id="ma-cantine">ma-cantine</span>.beta.gouv.fr</div>
        <div id="egalim">Pour une alimentatation saine, de qualité et plus durable dans nos assiettes grâce à EGAlim</div>
      </div>
    </router-link>
    <router-link :to="{ name: 'keypoints' }" class="navbar-item">Mesures phares</router-link>
    <a class="navbar-item" href="https://beta.gouv.fr/startups/egalim.html" target="_blank">A propos</a>
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
  padding: 10px 50px;
}

#landing {
  display: flex;
}

#Marianne {
  height: 75px;
}

#logo {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  margin-left: 30px;
  text-align: left;
  width: 300px;
  text-decoration: none;
}

#ma-cantine-beta-gouv {
  font-style: italic;
  font-weight: 200;
  font-size: 25px;
  line-height: 29px;
  color: rgba(64, 64, 64, 0.85);
}

#ma-cantine {
  font-weight: bold;
  color: #F7B48E;
}

#egalim {
  font-size: 11px;
  font-weight: 600;
  line-height: 15px;
  color: rgba(0,0,0,0.83);
}

.navbar-item {
  margin: auto 0;
  border-radius: 25px;
  padding: 15px;
  font-size: 17px;
  line-height: 20px;
  color: rgba(64, 64, 64, 0.85);
}

.navbar-item:hover {
  color: white;
  background-color: #F7B48E;
}
</style>
