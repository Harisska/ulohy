ALTER TABLE RegistrarInvoice ADD invoice_prefix VARCHAR(255);

UPDATE RegistrarInvoice riv SET invoice_prefix = r.Handle || '–' || z.fqdn FROM Registrar r JOIN zone z ON riv.Zone = z.id WHERE riv.RegistrarID = r.ID;
/* alternativou by bylo i použít CONCAT je  sice pomalejsi ale kontroluje typ */
COPY (
    SELECT ID, RegistrarID, Zone, FromDate, toDate, invoice_prefix
    FROM RegistrarInvoice
) TO '/tmp/registrarinvoice.csv' WITH CSV HEADER; 