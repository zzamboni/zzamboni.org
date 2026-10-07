# OpenAI API usage reporting

`openai-usage.yml` is a reusable workflow and can also be run manually. The summary
and feature-image workflows call it after their generation jobs, including when
those jobs fail. The report appears in the Actions run summary.

Configure under repository **Settings → Secrets and variables → Actions**:

| Kind | Name | Value |
| --- | --- | --- |
| Secret | `OPENAI_ADMIN_KEY` | OpenAI organization admin key with access to the Costs API |
| Optional variable | `OPENAI_CREDIT_DATE` | Latest credit purchase date, `YYYY-MM-DD` |
| Optional variable | `OPENAI_CREDIT_AMOUNT` | Latest purchase amount in USD, e.g. `5` |

The ordinary `OPENAI_API_KEY` used for generation is not substituted for the
admin key. Only the reporting job receives the admin secret.

Without purchase variables, the report shows today's and month-to-date
organization-wide costs, using UTC periods. A valid purchase date also displays
expiry, computed as one calendar year later (February 29 becomes February 28).
Both valid purchase variables enable an estimate: purchase amount minus costs
since the purchase date, floored at zero. An expired purchase has zero remaining
credit. Missing credentials, invalid metadata, or API failures are reported
without blocking generation. Low credit and expiry within 30 days produce warnings.

The estimate describes only the latest purchase, not the actual prepaid ledger;
older grants, overlapping reloads, adjustments, and costs earlier on the purchase
day can make it inaccurate. Billing data may lag recent requests. Daily Costs API
buckets do not establish an exact cost for the current workflow run.

Another workflow can call it with:

```yaml
  openai-usage:
    needs: generation
    if: ${{ always() && !cancelled() }}
    permissions:
      contents: read
    uses: ./.github/workflows/openai-usage.yml
    secrets:
      OPENAI_ADMIN_KEY: ${{ secrets.OPENAI_ADMIN_KEY }}
```

API reference: https://developers.openai.com/api/reference/resources/admin/subresources/organization/subresources/usage/methods/costs

Validation: `python -m unittest discover -s scripts/tests -p test_openai_usage.py`.
