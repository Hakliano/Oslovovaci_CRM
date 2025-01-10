<!-- Formulář pro filtrování -->
<form method="get" class="mb-4">
    <div class="row">
      <div class="col-md-4">
        <label for="partner">Jméno</label>
        <input type="text" name="partner" id="partner" class="form-control" placeholder="Zadejte část jména"
               value="{{ partner_name }}">
    </div>  
    <div class="row">
        <div class="col-md-4">
          <label for="partner">Jednatel</label>
          <input type="text" name="Jednatel" id="partner" class="form-control" placeholder="Zadejte část jména"
                 value="{{ partner_jednatel }}">
      </div>  
      <div class="row">
        <div class="col-md-4">
          <label for="partner">Email</label>
          <input type="text" name="Email" id="partner" class="form-control" placeholder="Zadejte část Emailu"
                 value="{{ partner_email }}">
      </div>  
          
        
    </div>
    <button type="submit" class="btn btn-primary mt-3">Filtrovat</button>
</form>