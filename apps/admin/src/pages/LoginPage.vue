<template>
  <div class="auth-shell">
    <v-card class="auth-card" elevation="0">
      <p class="eyebrow">Admin access</p>
      <h1>Ingresa al panel de localizaciones</h1>
      <p class="copy">Autenticación propia lista para conectarse con FastAPI y el usuario seeded.</p>

      <v-form class="auth-form">
        <v-text-field label="Email" variant="outlined" model-value="admin@example.com" />
        <v-text-field label="Password" type="password" variant="outlined" model-value="ChangeMe123!" />
        <v-btn color="primary" size="large" block>Entrar</v-btn>
      </v-form>
    </v-card>
  </div>
</template>

