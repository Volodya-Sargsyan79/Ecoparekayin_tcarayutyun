<template>
    <div class="container_employee">
        <div class="columns is-multiline">
            <div class="column is-12">
                <section class="section">
                    <div class="container_employee">
                        <div class="columns is-multiline">
                            <div class="column is-2">
                                <div class="box">
                                    <div class="has-text-centered">
                                        <h2 class="mt-4 mb-4">
                                            <span class="is-size-2">
                                                <strong>ԷՊԾ</strong>
                                            </span>
                                            <br/>
                                            <span class="is-size-4">
                                                <strong>տեղամասերի հերթափոխերի գրաֆիկ</strong>
                                            </span>
                                             
                                        </h2>
                                    </div>
                                    <div class="has-text-centered">
                                        <Filters />                                     
                                    </div>
                                </div>
                            </div>
                            <div class="column is-10">
                                <!-- FORM CHANGES BASED ON URL -->
                                <router-view />
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div> 
</template>

<script>
import Filters from '@/components/nav/Filters.vue';

export default {
    name: 'ShitInfo',
    components: { Filters }
}
</script>