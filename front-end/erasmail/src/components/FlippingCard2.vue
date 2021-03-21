<template>
  <div class="flip-card">
    <div class="flip-card-inner">
      <div class="box flip-card-front has-background-success-light">
        <div class="hero is-small">
          <div class="hero-head">
            <p class="title has-text-info is-size-4-fullhd is-size-4-widescreen is-size-4-desktop is-size-5-tablet">
              {{ frontTitle }}
            </p>
          </div>
          <div class="hero-foot">
            <p class="subtitle is-size-6-fullhd is-size-6-widescreen is-size-7-desktop is-size-7-tablet">
              {{ frontData }}
            </p>
          </div>
        </div>
      </div>
      <div class="box flip-card-back">
        <div class="hero is-small">
          <div class="hero-head">
            <p class=" title is-size-5-fullhd is-size-6-widescreen is-size-6-desktop is-size-6-tablet" >
              {{ backTitle }}
            </p>
          </div>

          <div class="hero-foot">
            <p class="subtitle is-size-6-fullhd is-size-7-widescreen is-size-7-desktop is-size-7-tablet" >
              {{ backData }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FlippingCard",
  props: {
    frontTitle: String,
    frontData: String,
    backTitle: String,
    backData: String
  }
};
</script>

<style scoped type="text/css">
/* The flip card container - set the width and height to whatever you want. We have added the border property to demonstrate that the flip itself goes out of the box on hover (remove perspective if you don't want the 3D effect */
.flip-card {
  background-color: transparent;
  width: 100%;
  height: 22vh;
  /* border: 1px solid #f1f1f1; */
  perspective: 1000px; /* Remove this if you don't want the 3D effect */
}

/* comment mettre une limite virtuelle pour hero-head à 30% de la height ? */
/* comment virer le height 200 px ? */
.hero-foot {
  position: fixed;
  bottom: 0;
  left: 0;
}

/* .subtitle {
  font-size: 1.9vh;
} */
.hero {
  height: 100%;
}

/* This container is needed to position the front and back side */
.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
  cursor: pointer;
}

/* Do an horizontal flip when you move the mouse over the flip box container */
.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}

/* Position the front and back side */
.flip-card-front,
.flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden; /* Safari */
  backface-visibility: hidden;
}

/* Style the front side (fallback if image is missing) */
.flip-card-front {
  background-color: whitesmoke;
  color: black;
}

/* Style the back side */
.flip-card-back {
  background-color: lightgreen;
  color: white;
  transform: rotateY(180deg);
}
</style>