<template>
  <div class="page-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">Operations</p>
        <h1>Location Management Admin</h1>
      </div>
      <v-btn color="secondary" to="/locations">Gestionar ubicaciones</v-btn>
    </header>

    <section class="stats-grid">
      <v-card class="stat-card" elevation="0">
        <span>Ubicaciones activas</span>
        <strong>128</strong>
      </v-card>
      <v-card class="stat-card" elevation="0">
        <span>Importaciones del mes</span>
        <strong>14</strong>
      </v-card>
      <v-card class="stat-card" elevation="0">
        <span>Categorías disponibles</span>
        <strong>5</strong>
      </v-card>
    </section>
  </div>
</template>

