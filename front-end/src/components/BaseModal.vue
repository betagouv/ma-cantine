<template>
  <div id="modal" @click.self="$emit('closeModal')" role="dialog" aria-labelledby="modal-title">
    <div id="modal-content">
      <button class="close" @click="$emit('closeModal')" aria-label="Fermer" title="Fermer"><i class="fas fa-times"></i></button>
      <slot/>
    </div>
  </div>
</template>

<style scoped lang="scss">
  #modal {
    position: fixed;
    z-index: 1;
    padding-top: 150px;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
  }

  #modal-content {
    margin: auto;
    padding: 50px;
    width: 45%;
    border: dotted 1px $yellow;
    border-radius: 4px;
    background-color: $light-yellow;
    overflow-y: auto;
    max-height: calc(100vh - 300px);
  }

  .close {
    float: right;
    cursor: pointer;
    border: none;
    background-color: transparent;

    .fa-times {
      width: 25px;
      height: 25px;
      color: $grey;
    }
  }

  .close:hover {
    .fa-times:hover {
      color: $light-grey;
    }
  }

  @media (max-width: 750px) {
    #modal {
      z-index: 2000;
      padding-top: 20px;
    }

    #modal-content {
      width: 70%;
      max-height: calc(100vh - 150px);
    }
  }
</style>
