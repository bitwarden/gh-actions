import * as core from '@actions/core';
import { AzureCliCredential } from '@azure/identity';
import { SecretClient } from '@azure/keyvault-secrets';

async function run(): Promise<void> {
  try {
    const keyvault = core.getInput('keyvault', { required: true });
    const secretsInput = core.getInput('secrets', { required: true });
    const secretNames = secretsInput
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);

    const credential = new AzureCliCredential();
    const client = new SecretClient(
      `https://${keyvault}.vault.azure.net`,
      credential,
    );

    for (const secretName of secretNames) {
      const secret = await client.getSecret(secretName);
      if (secret.value === undefined) {
        throw new Error(`Secret "${secretName}" has no value`);
      }
      core.setSecret(secret.value);
      core.setOutput(secretName, secret.value);
    }
  } catch (error) {
    core.setFailed(error instanceof Error ? error.message : String(error));
  }
}

run();
