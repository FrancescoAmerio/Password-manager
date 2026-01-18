Struttura dei branch

Questo repository contiene due branch principali, che rappresentano due diverse modalità di utilizzo dell’applicazione:

main:

Contiene la versione dell’applicazione che utilizza MySQL come database.
Questa versione è pensata per un ambiente di sviluppo o per scenari in cui è disponibile un server database esterno.

branchSqlite:

Contiene la versione dell’applicazione che utilizza SQLite come database su file.
Questa versione è stata utilizzata insieme al file PasswordManager.spec per creare un eseguibile (.exe) tramite PyInstaller, in modo da poter utilizzare l’applicazione su qualsiasi PC Windows senza dover installare dipendenze aggiuntive (come Python o un database server).
