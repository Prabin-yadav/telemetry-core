CRUMB=$(curl -c /tmp/cookies.txt -b /tmp/cookies.txt -u prabin:TempPass-ChangeMe-826! -s 'http://localhost:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)')
echo "Crumb: $CRUMB"
curl -c /tmp/cookies.txt -b /tmp/cookies.txt -u prabin:TempPass-ChangeMe-826! -H "$CRUMB" -X POST http://localhost:8080/reload
echo "Triggering build..."
sleep 2
curl -c /tmp/cookies.txt -b /tmp/cookies.txt -u prabin:TempPass-ChangeMe-826! -H "$CRUMB" -X POST http://localhost:8080/job/Telemetry_Core_Pipeline/build
echo "Checking build status..."
