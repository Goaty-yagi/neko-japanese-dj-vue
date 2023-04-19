<template>
  <i class='start-icon' :class='iconSelector()'></i>
</template>

<script>
export default {
    props: [
        "grade"
    ],
    daat() {
        return {

        }
    },
    methods: {
        iconSelector() {
            switch(this.grade) {
                case '超初級':
                    return "fas fa-dice-one"
                case '初級１':
                    return "fas fa-dice-two"
                case '初級２':
                    return "fas fa-dice-three"
                case '中級':
                    return "fas fa-dice-four"
                case '上級':
                    return "fas fa-dice-five"
            }
            
        }
    }
}
</script>

<style>

</style>